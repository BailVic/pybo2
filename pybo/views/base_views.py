from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404

from ..models import Question, Answer, Category, QuestionCount


def index(request, category_name='qna'):
    """
        pybo 목록 출력
        """
    # 입력 인자
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    category_list = Category.objects.all()
    category = get_object_or_404(Category, name=category_name)
    question_list = Question.objects.filter(category=category)

    # 정렬

    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')

    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')

    else:  # recent
        question_list = Question.objects.order_by('-create_date')

    if kw:
         question_list = question_list.filter(
             Q(subject__icontains=kw) |  # 제목검색
             Q(content__icontains=kw) |  # 내용검색
             Q(author__username__icontains=kw) |  # 질문 글쓴이검색
             Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
         ).distinct()

    # 페이징 처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여 주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so,
               'category_list': category_list, 'category': category} #page와 kw가 추가됨
    return render(request, 'pybo/question_list.html', context)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def detail(request, question_id):
    """
        pybo 내용 출력
        """
    question = get_object_or_404(Question, pk=question_id)

    # 입력 인자
    page_d = request.GET.get('page', '1')
    so_d = request.GET.get('so', 'recent')  # 정렬기준

    # 조회수
    ip = get_client_ip(request)
    cnt = QuestionCount.objects.filter(ip=ip, question=question).count()
    if cnt == 0:
        qc = QuestionCount(ip=ip, question=question)
        qc.save()
        if question.view_count:
            question.view_count += 1
        else:
            question.view_count = 1
        question.save()

    if so_d == 'recommend':
        answer_set = Answer.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')

    else:  # recent
        answer_set = Answer.objects.order_by('-create_date')

    # 조회
    #answer_list = Answer.objects.order_by('-create_date')

    # 페이징 처리
    paginator_a = Paginator(answer_set, 10)
    page_obj_a = paginator_a.get_page(page_d)

    context = {'question': question, 'answer_set': page_obj_a, 'page': page_d, 'so': so_d}
    return render(request, 'pybo/question_detail.html', context)


