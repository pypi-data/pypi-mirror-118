from pathlib import Path
from tqdm import tqdm

import click
from requests.exceptions import ProxyError, SSLError, ConnectionError

from sinaspider import UserConfig, Artist, Weibo
from sinaspider.helper import logger


@click.group()
def script():
    pass


@script.command()
@click.option('--fetch_weibo', '-w', is_flag=True)
@click.option('--fetch_relation', '-r', is_flag=True)
@click.option('--download_dir', '-d')
def loop(fetch_weibo, fetch_relation, download_dir):
    for uc in UserConfig.table.find(order_by='weibo_update_at'):
        uc = UserConfig(uc)
        while True:
            try:
                if fetch_weibo:
                    uc.fetch_weibo(download_dir)
                if fetch_relation:
                    uc.fetch_relation()
                break

            except (ProxyError, SSLError, ConnectionError):
                logger.warning('Internet seems broken, sleeping...')
                for i in range(600):
                    print(f'sleeping {600 - i - 1}', end='\r')
                continue


@script.command()
@click.argument('paths', nargs=-1, type=click.Path(exists=True, path_type=Path))
def meta(paths: list[Path]):
    from exiftool import ExifTool
    with ExifTool() as et:
        imgs = []
        for path in paths:
            if path.is_file():
                imgs.append(path)
            else:
                imgs.extend(path.rglob("*"))

        for img in tqdm(imgs):
            if not img.is_file():
                continue
            try:
                meta = et.get_metadata(str(img))
            except ValueError as e:
                logger.error(f'{e}:img')
                continue
            user_info, weibo_info = {}, {}
            if meta.get('XMP:ImageSupplierName') != 'Weibo':
                continue
            if user_id := meta.get('XMP:ImageSupplierID'):
                user_info = Artist(user_id).gen_meta()
            if weibo_id := meta.get('XMP:ImageUniqueID'):
                sn = meta.get('XMP:ImageSeriesNumber', 0)
                weibo_info = Weibo(weibo_id).gen_meta(sn)
            assert weibo_info | user_info == user_info | weibo_info
            tags = weibo_info | user_info
            et.set_tags(tags, str(img))


