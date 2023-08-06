import re

from loguru import logger
from imgmeta.helper import get_addr 



class ImageMetaUpdate:
    def __init__(self, meta):
        self.meta = meta.copy()
        self.filename = meta['File:FileName']
        while True:
            original = self.meta
            self.loop()
            if original == self.meta:
                break

    def loop(self):
        self.fix_meta()
        description = gen_description(self.meta)
        title = gen_title(self.meta)
        self._assign_multi_tag('XMP:Title', 'XMP:Caption', title)
        self._assign_multi_tag(
            'XMP:Description', 'XMP:UserComment', description)
        self.write_location()
        self.assign_raw_file_name()

    def assign_raw_file_name(self):
        raw_meta = self.meta.get('XMP:RawFileName')
        filename = self.meta['File:FileName']
        if raw_meta and raw_meta != filename:
            return
        raw_file_name = get_raw_file_name(self.meta)
        if raw_file_name:
            self.meta['XMP:RawFileName'] = raw_file_name

    def _gen_location(self):
        location = self.meta.get('XMP:Location')
        if location == '无':
            location = ''
            self.meta['XMP:Location'] = location
        if not location:
            return
        address = Locator().get_addr(location)
        if not address:
            logger.warning(f'{self.filename}=>Cannot locate {location}')
        return address

    def write_location(self):
        address = self._gen_location()
        if not address:
            return
        composite = self.meta.get('Composite:GPSPosition')
        geography = self.meta.get('XMP:Geography')
        if composite:
            if not geography:
                return
            com = [float(x) for x in composite.split()]
            geo = [float(x) for x in geography.split()]
            for x, y in zip(com, geo):
                if x - y > 1e-9:
                    logger.warning(f'{self.filename}:composite {composite} not eq geography {geography}')
                    return
        latitude = f"{address['latitude']:.7f}"
        longitude = f"{address['longitude']:.7f}"
        latitude, longitude = float(latitude), float(longitude)
        self.meta['XMP:GPSLatitude'] = latitude
        self.meta['XMP:GPSLongitude'] = longitude
        self.meta['XMP:Geography'] = f'{latitude} {longitude}'

    def fix_meta(self):
        tuple_tag_to_move = [
            (':BaseURL', 'XMP:SourceURL'),
            (':ImageDescription', 'XMP:Description'),
            ('IPTC:Keywords', 'XMP:Subject'),
            ('QuickTime:Artist', 'XMP:Artist'),
            ('EXIF:Artist', 'XMP:Artist'),
            ('PNG:Artist', 'XMP:Artist'),
            ('IPTC:Source', 'XMP:Source'),
            ('PNG:Source', 'XMP:Source'),
            ('EXIF:ImageUnique', 'XMP:ImageUniqueID')
        ]
        time_to_move = [
            ':DateTimeOriginal',
            ':EXIF:CreateDate',
            ':IPTC:DateCreated',
        ]

        for src_tag, dst_tag in tuple_tag_to_move:
            self.move_tag(src_tag, dst_tag)
        for src_tag in time_to_move:
            self.move_tag(src_tag, 'XMP:DateCreated', diff_print=False)
        self.copy_tag('File:FileName', 'XMP:RawFileName', diff_print=False)
        if self.meta['File:MIMEType'] == 'video/mp4':
            self.copy_tag('XMP:DateCreated', 'QuickTime:CreateDate')
            self.copy_tag('XMP:Title', 'QuickTime:Title', diff_ignore=True)

        for k, v in self.meta.items():
            if str(v) in ['None', '无']:
                self.meta[k] = ''

    def _assign_multi_tag(self, tag, tag_aux, value):
        v = self.meta.get(tag, '')
        v_aux = self.meta.get(tag_aux, '')
        if v and v != v_aux:
            logger.warning(f'{self.filename}=>>>{tag}:{v} not equal {tag_aux}:{v_aux}')
        else:
            self.meta[tag] = value
            self.meta[tag_aux] = value

    def move_tag(self, src_tag, dst_tag, **kwargs):
        write = self._move_or_copy_tag(
            src_tag, dst_tag, is_copy=False, **kwargs)
        if write:
            self.meta.update(write)

    def copy_tag(self, src_tag, dst_tag, **kwargs):
        write = self._move_or_copy_tag(
            src_tag, dst_tag, is_copy=True, **kwargs)
        if write:
            self.meta.update(write)

    def _move_or_copy_tag(self, src_tag, dst_tag, is_copy=False, diff_print=True, diff_ignore=False):
        assert (src_tag != dst_tag)
        src_meta, src_values = self._fetch_tag(src_tag)
        dst_meta, dst_values = self._fetch_tag(dst_tag)
        assert (len(dst_meta) <= 1)
        if not src_values:
            return
        if len(src_values) > 1:
            logger.warning(f"{self.meta.get('SourceFile')}: Multi values of src_meta => {src_meta}")
            return
        if dst_values and dst_values[0] != src_values[0] and not diff_ignore:
            if diff_print:
                logger.warning(
                    f"{self.meta.get('SourceFile')}: Values not same =>src_meta:{src_meta},dst_meta:{dst_meta}")
            if dst_values[0] != '0000:00:00 00:00:00':
                return
        value = src_values[0]
        dst_update = {dst_tag: value}
        src_remove = {k: '' for k in src_meta}
        if is_copy:
            return dst_update
        else:
            return dict(**dst_update, **src_remove)

    def _fetch_tag(self, tag):
        sub_meta = {k: v for k, v in self.meta.items() if k.endswith(tag)}
        values = set(str(v) for v in sub_meta.values())
        values = list(values)
        return sub_meta, values


def gen_title(meta):
    artist = meta.get('XMP:Artist') or meta.get('XMP:ImageSupplierName')
    time = meta.get('XMP:DateCreated')
    sn = meta.get('XMP:SeriesNumber')
    if not artist:
        return ''
    if not time:
        return artist
    time = re.split('[: ]', time)
    year, month, day, *_ = time
    year = year[-2:]
    title = '-'.join([artist, year, month, day])
    if sn:
        title = f'{title}-{sn}'
    return title


def gen_description(meta):
    source = meta.get('XMP:Source') or meta.get('XMP:ImageSupplierName')
    a, c = meta.get('XMP:Artist', ''), meta.get('XMP:Creator', '')
    creator = ' '.join([a, c]) if a not in c else c
    url = meta.get('XMP:BlogURL', '') or meta.get('XMP:ImageCreatorID', '')
    text = meta.get('XMP:BlogTitle', '')
    user_info = '-'.join(str(x) for x in [source, creator] if x)
    description = '  '.join(str(x).replace('\n', '\t')
                            for x in [text, url, user_info] if x)

    return description


def get_raw_file_name(meta):
    image_supplier_name = meta.get('XMP:ImageSupplierName')
    image_unique_id = meta.get('XMP:ImageUniqueID')
    image_supplier_id = meta.get('XMP:ImageSupplierID')
    sn = meta.get('XMP:SeriesNumber')
    ext = meta.get('File:FileTypeExtension').lower()
    if not image_unique_id:
        return
    if image_supplier_name == 'Weibo':
        raw_file_name = f'{image_supplier_id}_{image_unique_id}'
        raw_file_name += f'_{sn}.{ext}' if sn else f'.{ext}'
        return raw_file_name
