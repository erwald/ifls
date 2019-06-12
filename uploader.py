from InstagramAPI import InstagramAPI
from PIL import Image
import random
import yaml
import os
import argparse

dirs = ['candidates']
[os.makedirs(d) for d in dirs if not os.path.exists(d)]

# Parse arguments.
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dry-run', action='store_true',
                    help='runs drily, iow without actually posting any images')
args = parser.parse_args()

conf = yaml.load(open('config.yml'))
insta_username = conf['instagram']['user']
insta_password = conf['instagram']['password']

instagram_api = InstagramAPI(insta_username, insta_password)

if not args.dry_run:
    instagram_api.login()

# Load candidates file.
candidates_file_path = 'candidates.yml'
if os.path.isfile(candidates_file_path):
    candidates = yaml.load(open(candidates_file_path))

    print(f"Loaded candidates: {candidates}")
else:
    print("Couldn't find any candidate photos ...")

# Filter out candidates that have already been posted, and then pick the one
# with the highest score (as given by the neural network).
users_with_post = set([c[1] for c in candidates if c[3]])
unposted_candidates = [c for c in candidates if not c[1] in users_with_post]
candidate = sorted(unposted_candidates, key=lambda c: c[2])[-1]
photo_filename = candidate[0]
user = candidate[1]

antecedent = random.sample(
    ['📷', '📸', 'Photo', 'By', 'Author', '🤳🏿', '🤳🏽', '🤳🏻'], 1)[0]
caption = f"{antecedent}: @{user}"
photo_path = f"./candidates/{photo_filename}"

print(photo_filename)
print(photo_path)
print(caption)

if not args.dry_run:
    # Remove EXIF data.
    image = Image.open(photo_path)
    image.save(photo_path)

    # Upload.
    instagram_api.uploadPhoto(photo_path, caption=caption)

    # Update the candidates file to show that the photo has been posted.
    candidate[3] = True  # Edit the candidate in-place.
    yaml.dump(candidates, open(candidates_file_path, 'w'))
