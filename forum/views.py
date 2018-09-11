# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-08-15

from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from qiniu import Auth
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins, generics
from rest_framework.permissions import AllowAny
from .models import *
from rewrite.exceptions import FoundPostFailed
from account.models import LoginUser
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    )
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from django.http import HttpResponse
from account.permissions import IsOwnerOrReadOnly,IsUserOrReadOnly
from rewrite.authentication import CsrfExemptSessionAuthentication
from rewrite.pagination import Pagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import F
from datetime import datetime,timedelta
from django.db.models import Count
import random

# 发帖
class PostPublishView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PyPostPublishSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get_tag(self, tag_id):
        try:
            return Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            raise NotFound("30004Not found the tag.")

    def post(self, request):
        # 已登录用户发帖
        serializer = PyPostPublishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data['title']
            content = serializer.validated_data['content']
            tagids = serializer.validated_data['tag'].split(";")
            passage = Post.objects.create(title=title, content=content, owner=request.user)
            # passage.save()

            for i in tagids:
                try:
                    tag = self.get_tag(int(i))
                    passage.tags.add(tag)  
                except:
                    msg = Response({
                    'error': 1,
                    'message': 'Tag(Tag id,int) is separated by comma'
                    }, HTTP_400_BAD_REQUEST)
                    return msg
            passage.save()

            msg = Response({
                'error': 0,
                'data': PyPostDetailSerializer(passage, context={'request': request}).data,
                'message': 'Success to publish the post.'
            }, HTTP_201_CREATED)
            return msg


# 获取全部帖子并展示
class PostListView(generics.ListAPIView):
    """
       未认证用户允许获取
    """
    permission_classes = (AllowAny,)
    # authentication_classes = (MyAuthentication, )
    serializer_class = PostListSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 筛选图书，筛选条件：交换状态、地点、作者国家、语言、类型
    # filter_fields = ('status', 'place', 'country', 'language', 'types')
    # ordering_fields = ('level', 'place')
    search_fields = ('title', )

    def get_queryset(self):
        queryset = Post.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset.order_by('-created_at')


# 某个帖子详情
class PostDetailView(generics.RetrieveDestroyAPIView):
    """
       未认证用户允许获取，已认证用户允许获取与删除自己的帖子
    """
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    serializer_class = PyPostDetailSerializer
    queryset = Post.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            cont = self.retrieve(request, *args, **kwargs)
            msg = Response(data={
                'error': 0,
                'data': cont.data,
            }, status=HTTP_200_OK)
        except Http404:  # 获取失败，没有找到对应数据
            raise FoundPostFailed
        else:
            return msg

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# 某个帖子详情
# class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     '''
#     get:
#         获取文章信息
#
#     put:
#         登录用户更新本人所发文章内容
#
#     delete:
#         登录用户删除本人整篇文章
#
#     '''
#
#     authentication_classes = (CsrfExemptSessionAuthentication,)
#     permission_classes = (IsOwnerOrReadOnly,IsAuthenticated)
#     serializer_class = PyPostDetailSerializer
#     queryset = Post.objects.all()
#     lookup_field = 'id'
#     lookup_url_kwarg = 'pid'


# 返回登录用户发布的所有帖子
class PostOfUserListView(generics.ListAPIView):
    """
       返回已认证用户的所有帖子
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    serializer_class = PostListSerializer
    pagination_class = Pagination

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(owner=user)
        return queryset.order_by('-created_at')

class PostNewListView(generics.ListAPIView):
    '''新发布的文章，每页10条，后面接 ?page=1 则为第一页。返回信息中有下一页链接。'''
    authentication_classes = (CsrfExemptSessionAuthentication,)
    serializer_class = PostListSerializer
    pagination_class = Pagination

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-created_at')[:40]
        return queryset

class PostHotListView(generics.ListAPIView):
    '''最热文章(点赞数最多)，每页10条，后面接 ?page=1 则为第一页。返回信息中有下一页 链接。'''
    authentication_classes = (CsrfExemptSessionAuthentication,)
    serializer_class = PostListSerializer
    pagination_class = Pagination

    def get_queryset(self):

        queryset = Post.objects.all().order_by('like')[:40]
        return queryset

class PostRecentHotListView(generics.ListAPIView):
    '''热榜文章(最近三天点赞数最多)，每页10条，后面接 ?page=1 则为第一页。返回信息中 有下一页链接。'''
    authentication_classes = (CsrfExemptSessionAuthentication,)
    serializer_class = PostListSerializer
    pagination_class = Pagination

    def get_queryset(self):

        today = datetime.now()
        
        likes = LikeOrDis.objects.filter(created_at__range=(today - timedelta(days=3),today)). \
            exclude(userprefer__contains='-').values('post_id'). \
            annotate(count=Count('id')).order_by('-count').values('post')

        post_ids = [] 
        for i in likes:
            post_ids.append(i['post'])

        queryset = Post.objects.filter(id__in=post_ids).order_by('-like')[:40] 
        return queryset


class PostTagListView(APIView):
    '''根据 tag_id 获取拥有该tag的所有文章'''
    authentication_classes = (CsrfExemptSessionAuthentication,)
    serializer_class = PostListSerializer
    pagination_class = Pagination

    def get_tag(self,tag_id):
        try:
            return Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            raise NotFound("30004Not found the tag.")

    def get(self,request,tag_id):
        tag = self.get_tag(int(tag_id))
        queryset = Post.objects.filter(tags = tag_id)
        s = PostListSerializer(queryset,many=True,context={'request': request})
        return Response(s.data)


# 上传图片
class PostImageUploadView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UploadPostImageSerializer

    def post(self, request):
        serializer = UploadPostImageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            image = serializer.validated_data['image']
            images = PostImage.objects.create(image=image)
            images.save()
            msg = Response({
                'error': 0,
                'data': {'image': images.get_img_url()},
                'message': 'Success to upload the image'
            }, HTTP_201_CREATED)
            return msg


class LikeOrDisDetailView(generics.RetrieveUpdateDestroyAPIView):

    '''
    get:
        已登录用户获取自己是否赞/踩这个帖子

    put:
        已登录用户更新自己对一篇文章喜好程度

    delete:
        已登录用户取消喜好

    '''
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeOrDisDetailSerializer
    queryset = LikeOrDis.objects.all()

    def get(self, request, pid):

        queryset = LikeOrDis.objects.filter(post_id = pid,user = request.user)
        s = LikeOrDisDetailSerializer(queryset,many=True,context={'request': request})
        return Response(s.data)

    def put(self,request,pid):

        s = LikeOrDisDetailSerializer(data=request.data)
        
        if s.is_valid(raise_exception=True):
            lod = LikeOrDis.objects.filter(post_id=pid ,user_id=request.user.id)
            if lod:

                prefer_old = LikeOrDis.objects.get(user=request.user, post_id=pid).userprefer
                userprefer = s.validated_data['userprefer']
                lod.update(userprefer = userprefer)

                check = userprefer * prefer_old
                if check<0:
                    if userprefer>0:
                        Post.objects.filter(id=pid).update(like=F('like')+1)
                        Post.objects.filter(id=pid).update(diss=F('diss')-1)

                    else:
                        Post.objects.filter(id=pid).update(like=F('like')-1)
                        Post.objects.filter(id=pid).update(diss=F('diss')+1)



                msg = Response({
                    'error': 0,
                    'message': 'Success to update'
                }, HTTP_200_OK)
            else:
                msg = Response({
                    'error': 0,
                    'message': 'Failed to update. You do not like it before.'
                }, HTTP_400_BAD_REQUEST)
        else:
            msg = Response({
                'error': 0,
                'message': 'BAD_REQUEST'
            }, HTTP_400_BAD_REQUEST)
        return msg

    def delete(self,request,pid):
        try:
            prefer_old = LikeOrDis.objects.get(user=request.user, post_id=pid).userprefer
            s = LikeOrDis.objects.get(post_id=pid,user_id=request.user.id)
            s.delete()
            
            if prefer_old>0:
                Post.objects.filter(id=pid).update(like=F('like')-1)
            else:
                Post.objects.filter(id=pid).update(diss=F('diss')-1)
            msg = Response({
                    'error': 0,
                    'message': 'Success to delete'
                }, HTTP_200_OK)
        except:
            msg = Response({
                'error': 0,
                'message': 'BAD_REQUEST'
            }, HTTP_400_BAD_REQUEST)

        return msg


class LikeOrDisListView(generics.ListAPIView):
    '''
    get:
        列出这篇文章所有点赞/踩的人
    '''

    permission_classes = (AllowAny,)
    queryset = LikeOrDis.objects.all()
    serializer_class = LikeOrDisListSerializer
    authentication_classes = ()

    def get(self,request,pid):
        queryset = LikeOrDis.objects.filter(post_id = pid)
        s = LikeOrDisListSerializer(queryset,many=True,context={'request': request})
        return Response(s.data)


class LikeOrDisPostView(generics.CreateAPIView):

    '''
    post:
        已登录用户赞/踩一个帖子
    
    '''

    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeOrDisPostSerializer

    def perform_create(self, serializer):

        post = serializer.validated_data['post']
        prefer = serializer.validated_data['userprefer']

        if prefer>0:
            Post.objects.filter(id=post.id).update(like=F('like')+1)
        else:
            Post.objects.filter(id=post.id).update(diss=F('diss')+1)
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post', '')
        user = request.user
        res = LikeOrDis.objects.filter(user=user, post_id=post_id)

        if res:
            msg = Response(data={
                'error': 0000,
                'message': 'You have already like it.'
            }, status=HTTP_400_BAD_REQUEST)
            return msg
        else:
            return self.create(request, *args, **kwargs)


class PostCommentsPostView(generics.CreateAPIView):
    '''
    post:
        已登录用户对一个文章发布评论
    '''

    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PostCommentPostSerializer

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class PostCommentsListView(generics.GenericAPIView):
    '''
    get:
        列出所有这篇文章的评论信息

    '''
    permission_classes = (AllowAny,)
    queryset = PostComments.objects.all()
    serializer_class = PostCommentListSerializer
    authentication_classes = ()

    def get(self, request, post_id):
        queryset = PostComments.objects.filter(post_id = post_id)
        s = PostCommentListSerializer(queryset,many=True,context={'request': request})
        return Response(s.data)


# 返回所有的标签
class TagListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TagDetailSerializer
    pagination_class = Pagination

    def get_queryset(self):
        quertset = Tag.objects.all()
        return quertset


class TokenReturnView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request):
        table = "0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
        q = Auth('7mn1axVj1LKGbSOpXI6RvqRkdI-zzzE2hnHwOK8I', '8AhoPQJH7U3GR-Cq_5slGVvzbXvF4P7F-P1Shhpv')
        bucket_name = 'android'
        pkey = "Posts/" + "".join(random.sample(table, 16)) + ".jpg"
        key = None
        policy = {
            "scope": "android",
            "saveKey": pkey,
        }
        token = q.upload_token(bucket_name, key, 3600, policy)
        return Response({
            'uptoken': token
        }, HTTP_200_OK)
