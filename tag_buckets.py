#!/usr/bin/python

"""
Add an additional tag to all S3 buckets
It adds the tag "name" with the name of the bucket.

Tags contain Tagset which contains Tag
"""

import boto
from boto.s3.connection import S3Connection


def tag(conn, name):
    try:
        bucket = conn.get_bucket(name)
    except:
        print('Error getting {}'.format(name))
        return
    if bucket is None:
        print("This bucket doesn't exist: {}".format(name))
    # we create a new tag
    tagset = boto.s3.tagging.TagSet()
    tagset.add_tag("name", name)

    # we keep current tags
    try:
        o_tags = bucket.get_tags()
    except:
        print('No existing tags for {}'.format(name))
        pass
    for o_tagset in o_tags:
        for o_tag in o_tagset:
            print('Tag: {}: {}'.format(o_tag.key, o_tag.value))
            tagset.add_tag(o_tag.key, o_tag.value)

    tags = boto.s3.tagging.Tags()
    tags.add_tag_set(tagset)

    # we set all the tags
    try:
        bucket.set_tags(tags)
    except:
        print('Error tagging {}'.format(name))
        pass


if __name__ == "__main__":
    conn = S3Connection()
    rs = conn.get_all_buckets()
    for b in rs:
        print('Tagging {}'.format(b.name))
        tag(conn, b.name)
