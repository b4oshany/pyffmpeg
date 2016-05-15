import click
from pyffmpeg import get_video_info, resize_video

@click.command()
@click.argument('video_file', type=click.Path('r'))
def getinfo(video_file):
    print get_video_info(video_file)



@click.command()
@click.argument('video_file', type=click.Path('r'))
@click.option('--save_as', default=None)
def resize_video(video_file, save_as=None):
    resize_video("milk-c#milk.mp4", save_as=save_as)
