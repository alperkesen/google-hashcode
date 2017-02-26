#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator


file = open("videos_worth_spreading.in","r")
[V, E, R, C, X] = map(int, file.readline().split())
video_sizes = list(map(int, file.readline().split()))


class Video(object):
    def __init__(self, pid, size):
        self.pid = pid
        self.size = size
        self.requests = {}

    def add_request(self, endpoint_id, num_requests):
        self.requests[endpoint_id] = num_requests


class Endpoint(object):
    def __init__(self, pid, data_lat):
        self.pid = pid
        self.data_lat = data_lat
        self.cac_lat = {}

    def add_cache_lat(self, cache_id, lat):
        self.cac_lat[cache_id] = lat
    

class Cache(object):
    max_capacity = X

    def __init__(self, pid):
        self.pid = pid
        self.size = 0
        self.video_list = []

    def add_video(self, video):
        self.size += video.size
        self.video_list.append(video)


videos = []
endpoints = [] 
caches = [Cache(c) for c in range(C)]
all_requests = {}


for v in range(V):
    video = Video(v, video_sizes[v])
    videos.append(video)

for e in range(E):
    endpoint_data = list(map(int, file.readline().split()))
    endpoint = Endpoint(e, endpoint_data[0])
    endpoints.append(endpoint)

    for num_connected_cache in range(endpoint_data[1]):
        endpoint.add_cache_lat(*map(int, file.readline().split()))

for r in range(R):
    request_data = list(map(int, file.readline().split()))
    videos[request_data[0]].add_request(request_data[1],request_data[2])
    all_requests[(request_data[0], request_data[1])] = request_data[2]


score = 0
requests_count = 0
sorted_requests = sorted(all_requests.items(), key=operator.itemgetter(1))[::-1]


for req in sorted_requests:
    requests_count += req[1]
    sorted_cac_lats = sorted(endpoints[req[0][1]].cac_lat.items(), key=operator.itemgetter(1))

    for num_caches in range(len(sorted_cac_lats)):
        if videos[req[0][0]].size + caches[sorted_cac_lats[num_caches][0]].size <= caches[sorted_cac_lats[num_caches][0]].max_capacity:
            caches[sorted_cac_lats[num_caches][0]].add_video(videos[req[0][0]])
            score += (endpoints[req[0][1]].data_lat-sorted_cac_lats[num_caches][1]) * req[1]
            break


score /= requests_count
score *= 1000

new_file = open("result.in", "w")

cache_count = 0
cache_info = {}

for cache in caches:
    if len(cache.video_list) > 0:
        cache_count += 1
    cache_info[cache.pid] = [y.pid for y in cache.video_list]


new_file.write(str(cache_count) + '\n')
for x in cache_info:
    if len(cache_info[x]) == 0:
        continue
    new_file.write(str(x))
    for y in cache_info[x]:
        new_file.write(" " + str(y))
    new_file.write('\n')





