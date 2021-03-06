from django.db import models
from datetime import datetime


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'城市')
    desc = models.CharField(max_length=200, verbose_name=u'描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'机构名称')
    # 机构描述
    desc = models.TextField(verbose_name=u'机构描述')
    category = models.TextField(verbose_name=u'机构类别', default='individual',
                                max_length=20,
                                choices=(
                                    ('individual', '个人'), ('college', '高校'),
                                    ('training_agency', '培训机构'))
                                )
    #添加一个标签，用于在首页上显示
    tag = models.CharField(default=u'hiahia', max_length=10, verbose_name=u'机构标签')

    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    image = models.ImageField(
        upload_to='org/%Y/%m',
        verbose_name=u'logo',
        max_length=100,
    )
    address = models.CharField(max_length=150, verbose_name=u'机构地址')
    city = models.ForeignKey(CityDict, on_delete=models.CASCADE,
                             verbose_name=u'所在城市')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    # 添加下面两个field，实现org-list页面的排序功能
    # 添加学习人数
    students = models.IntegerField(default=0, verbose_name=u'学生人数')
    # course_nums
    course_nums = models.IntegerField(default=0, verbose_name=u'课程数')

    class Meta:
        verbose_name = u'课程机构'
        verbose_name_plural = verbose_name

    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE,
                            verbose_name=u'所属机构')
    name = models.CharField(max_length=50, verbose_name=u'教师名称')
    work_years = models.IntegerField(default=0, verbose_name=u"工作年限")
    work_company = models.CharField(max_length=50, verbose_name=u"就职公司")
    work_position = models.CharField(max_length=50, verbose_name=u"公司职位")
    points = models.CharField(max_length=50, verbose_name=u"教学特点")
    age = models.IntegerField(default=21, verbose_name=u"年龄")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    image = models.ImageField(
        upload_to='teachers/%Y/%m',
        verbose_name=u'头像',
        max_length=100,
        default='',
    )
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_course_total_num(self):
        return self.course_set.count()