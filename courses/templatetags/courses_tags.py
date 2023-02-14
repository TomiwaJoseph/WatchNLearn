# from django import template
# import cv2, time, math
# # from mutagen.mp4 import MP4
# from django.utils import timezone

# register = template.Library()

# @register.filter
# def format_timesince(some_time):
#     now = timezone.now()
#     diff = now - some_time
#     if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
#         seconds = diff.seconds
#         if seconds == 1:
#             return str(seconds) + " second ago"
#         else:
#             return str(seconds) + " seconds ago"
#     if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
#         minutes = math.floor(diff.seconds/60)
#         if minutes == 1:
#             return str(minutes) + " minute ago"
#         else:
#             return str(minutes) + " minutes ago"
#     if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
#         hours = math.floor(diff.seconds/3600)
#         if hours == 1:
#             return str(hours) + " hour ago"
#         else:
#             return str(hours) + " hours ago"
#     if diff.days >= 1 and diff.days < 30:
#         days = diff.days
#         if days == 1:
#             return str(days) + " day ago"
#         else:
#             return str(days) + " days ago"
#     if diff.days >= 30 and diff.days < 365:
#         months = math.floor(diff.days/30)
#         if months == 1:
#             return str(months) + " month ago"
#         else:
#             return str(months) + " months ago"
#     if diff.days >= 365:
#         years =  math.floor(diff.days/365)
#         if years == 1:
#             return str(years) + " year ago"
#         else:
#             return str(years) + " years ago"

# @register.filter
# def check_star(stars):
#     return range(int(stars))

# @register.filter
# def get_course_duration(course):
#     all_modules = course.course_modules.all()
#     total_seconds = 0
#     all_content = [content for module in all_modules for content in module.modules_content.all()]
#     for video_file in all_content:
#         video_file_path = video_file.content_video.path
#         data = cv2.VideoCapture(video_file_path)
#         frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
#         fps = int(data.get(cv2.CAP_PROP_FPS))
#         if frames == 0.0 or fps == 0:
#             seconds = 0
#         else: seconds = int(frames/fps)
#         total_seconds += seconds
#     if total_seconds >= 3600:
#         return str(time.strftime("%Hh %Mm %Ss", time.gmtime(total_seconds)))
#     return str(time.strftime("%Mm %Ss", time.gmtime(total_seconds)))

# @register.filter
# def get_video_duration(video_file):
#     video_file_path = video_file.content_video.path
#     data = cv2.VideoCapture(video_file_path)
#     frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
#     fps = int(data.get(cv2.CAP_PROP_FPS))
#     if frames == 0.0 or fps == 0:
#         seconds = 0
#     else: seconds = int(frames/fps)
#     return str(time.strftime("%M:%S", time.gmtime(seconds)))

# #mutagen version of getting video length
# # def video_length(video_file):
# #     path = video_file.content_video.path
# #     video = MP4(path)
# #     video_length = video.info.length
# #     return str(time.strftime("%M:%S", time.gmtime(video_length)))
