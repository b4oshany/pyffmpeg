from pyffmpeg import get_video_info

@click.command()
@click.argument('video_file', type=click.Path('r'))
def getinfo(video_file):
    print get_video_info(video_file)
