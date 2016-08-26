from calendar import month_name
from blog.models import Post


def monthly_archives(request):
    if not Post.objects.count:
        return
    objects = Post.objects.order_by('-pub_date')
    months = []
    for object in objects:
        year = object.pub_date.year
        month = object.pub_date.month
        month_data = {'month': month_name[month],
                      'short': month_name[month][:3].lower(),
                      'year': year,
                      }
        if month_data in months:
            pass
        else:
            months.append(month_data)

    return {'months': months}