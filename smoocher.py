#!/bin/zsh

from instapy import InstaPy
from instapy import smart_run
import yaml

conf = yaml.load(open('config.yml'), Loader=yaml.FullLoader)
insta_username = conf['instagram']['user']
insta_password = conf['instagram']['password']

session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=True,
                  use_firefox=True)

with smart_run(session):
    session.set_action_delays(enabled=True,
                              like=5,
                              comment=10,
                              follow=10,
                              unfollow=10,
                              randomize=True,
                              random_range=(50, 200))
    session.set_quota_supervisor(enabled=True,
                                 sleep_after=['likes', 'comments_d', 'follows', 'unfollows', 'server_calls_h'], sleepyhead=True,
                                 stochastic_flow=True,
                                 peak_likes=(57, 585),
                                 peak_comments=(21, 182),
                                 peak_follows=(48, None),
                                 peak_unfollows=(35, 402),
                                 peak_server_calls=(None, 4700))
    session.set_relationship_bounds(enabled=True,
                                    delimit_by_numbers=True,
                                    max_followers=5000,
                                    min_followers=50,
                                    min_following=100)
    session.set_dont_unfollow_active_users(enabled=True, posts=10)

    users = ['der_greif', 'brownieartphoto', 'lagosphotofestival', 'sharjahart',
             'latinamericanfotografia', 'aklphotofestival', 'mfonfoto']
    session.set_user_interact(amount=4, randomize=True,
                              percentage=50, media='Photo')
    session.set_do_like(True, percentage=70)
    session.set_do_follow(True, percentage=100)
    session.interact_user_followers(users, amount=10, randomize=True)

    tags = ['humbleweekendz', 'humbleweekdayz', 'art',
            'photography', 'vsco', 'follow4follow', 'f4f']
    session.like_by_tags(tags, amount=6)
    session.follow_by_tags(tags, amount=4, randomize=True, interact=True)

    session.unfollow_users(amount=194, InstapyFollowed=(
        True, 'nonfollowers'), style='FIFO', unfollow_after=72*60*60, sleep_delay=501)

    session.like_by_feed(amount=14, randomize=True,
                         unfollow=False, interact=True)
