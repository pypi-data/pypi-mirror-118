from datetime import timedelta
from datetime import datetime
# import thtools
import os
import shutil
from thtools.thtools_base import list_dict2dict_list
import jinjafy
import openpyxl
from coursebox.core.projects_info import populate_student_report_results
from coursebox.core.info_paths import get_paths, semester_id, semester, year, today
from coursebox.core.info_paths import core_conf
# import six
# import pybtex.database.input.bibtex
# import pybtex.plugin
# import io


def xlsx_to_dicts(xlsx_file,sheet=None, as_dict_list=False):
    wb = openpyxl.load_workbook(xlsx_file, data_only=True)
    if not sheet:
        ws = wb.worksheets[0]
    else:
        ws = [ws for ws in wb.worksheets if ws.title == sheet]
        if len(ws) < 1:
            return None
        else:
            ws = ws.pop()
    dd = []
    key_cols = [j for j in range(ws.max_column) if ws.cell(row=1, column=j + 1).value is not None]
    for i in range(1, ws.max_row):
        rdict = {}
        if not any( [ws.cell(row=i+1, column=j+1).value is not None for j in key_cols] ):
            continue
        for j in key_cols:
            key = ws.cell(row=1, column=j+1).value
            if key is not None:
                key = key.strip() if isinstance(key,str) else key
                value = ws.cell(row=i + 1, column=j + 1).value
                value = value.strip() if isinstance(value,str) else value
                if isinstance(value, str):
                    if value == 'True':
                        value = True
                    if value == 'False':
                        value = False
                rdict[key] = value
        dd.append(rdict)

    if as_dict_list:
        dl = list_dict2dict_list(dd)
        for k in dl.keys():
            x = [v for v in dl[k].tolist() if v is not None]
            if len(x) == 1: x = x.pop()
            dl[k] = x
        dd = dl
    return dd

def get_enrolled_students():
    paths = get_paths()
    students = xlsx_to_dicts(paths['information.xlsx'], sheet='students')
    students2 = {}
    for s in students:
        s2 = {}
        if s['Study number']:
            s['Username'] = s['Study number']
        for k in s.keys():
            k2 = k.lower().replace(" ", "")
            if k2 == "studynumber": continue
            if k2 == "username":
                k2 = "id"
                if not s[k] or len(s[k]) == 0:
                    print("Bad study id: ")
                    print(s)
                    raise Exception("malformed course configuration file, bad student id")
            s2[k2] = s[k]

        id = s2['id']
        students2[id] = s2
    return students2


def get_file_dir_or_template(filepath, templatepath):
    thtools.ensure_dir_exists( os.path.dirname(filepath) )
    if not os.path.exists(os.path.dirname):
        shutil.copyfile(templatepath, filepath)


def get_instructors():
    paths = get_paths()
    instructors = xlsx_to_dicts(paths['information.xlsx'], sheet='instructors')
    return instructors

def continuing_education():
    return thtools.coursebox.core.info_paths.core_conf['continuing_education_mode']

def first_day_of_class(info):
    if continuing_education():
        first_day_of_class = datetime(year=year(), month=info['first-month'], day=info['first-day'], hour=info['hour'][0], minute=info['minute'][0])
    else:
        mo_first = datetime(year=year(), month=1 if semester() == 'spring' else 8, day=1, hour=13, minute=0)
        # scroll to monday
        while mo_first.weekday() != 0: #strftime('%A') is not 'Monday':
            mo_first += timedelta(days=1)
        # add 4 weeks to get into 13 week period
        for _ in range(4):
            mo_first += timedelta(days=7)

        dow = int(info.get('day_of_week', 1))
        while mo_first.weekday() != dow:
            mo_first += timedelta(days=1)

        first_day_of_class = mo_first
    return first_day_of_class


def find_tex_cite(s, start=0, key="\\cite"):
    txt = None
    i = s.find(key, start)
    if i < 0:
        return (i,None), None, None
    j = s.find("}", i)
    cite = s[i:j + 1]

    if cite.find("[") > 0:
        txt = cite[cite.find("[") + 1:cite.find("]")]

    reference = cite[cite.find("{") + 1:cite.find("}")]
    return (i, j), reference, txt

def lectures(info, pensum=None):
    ow = timedelta(days=7)
    d = first_day_of_class(info)

    holiday = int(info['holiday_week']) if "holiday_week" in info else (9 if semester() == "spring" else 6)
    paths = get_paths()
    lectures = []
    lecture_info = xlsx_to_dicts(paths['information.xlsx'], sheet='lectures')

    for lecture in lecture_info:
        em = lecture["resources"]
        r = []
        if em:
            ems = em.split("\n")
            for e in ems:
                e = e.strip()
                url = e[:e.find(" ")]
                description = e[e.find(" ") + 1:]
                shorturl = url[:url.find("/",url.find("."))]
                r.append( {'url': url, 'shorturl': shorturl, 'description': description})
        lecture["resources"] = r
        if pensum is not None:
            rd, html = lecture['reading'], ""
            while True:
                i = rd.find("\\cite")
                if i < 0: break
                j = rd.find("}", i)
                html += rd[:i]
                cite = rd[i:j + 1]
                rd = rd[j+1:]
                if cite.find("[") > 0:
                    sr = cite[cite.find("[")+1:cite.find("]")]
                else:
                    sr = None
                key = cite[cite.find("{")+1:cite.find("}")]
                html += "[<b>" + pensum[key]['label'] + "</b>" + (", " + sr if sr is not None else "") + "]"
                pensum[key]['suggested'] = True
            html += rd
            lecture['reading_html'] = html

    if continuing_education():
        ice = xlsx_to_dicts(paths['information.xlsx'], sheet='ce', as_dict_list=True)
        holiday = -1
        dd = [ice['day'][i] - ice['day'][i-1] for i in range(1, len(ice['day']))]
        dd.append(0)

    for i in range(0, len(lecture_info)):
        l = dict()
        l['year'] = d.year
        l['month'] = d.strftime('%B')
        l['day'] = d.day
        l['date'] = d
        l['preceded_by_holiday'] = i == holiday
        if not continuing_education():
            d = d + ow
            if i == holiday - 1: d = d + ow
            if d.month == 5 and d.day == 8: # grundlovsdag
                d += timedelta(days=4)
        else:
            d = d + timedelta(days=dd[i-0] if i > 1 else 0)
            d = d.replace(hour=ice['hour'][i-1], minute=ice['minute'][i-1])

        info = lecture_info[i]

        ir = info.get('reading', "")
        info['reading_long'] = ir.replace("C", "Chapter ") if ir else ""

        hwp =  info['homework_problems']
        info['homework_problems_long'] = hwp.replace("P", "Problem ") if hwp else ""
        if info["learning_objectives"]:
            info["learning_objectives"] = [s.strip() for s in info["learning_objectives"].split("\n")]
        l.update(info)
        lectures.append(l)
    return lectures, pensum

def get_forum(paths):
    a = xlsx_to_dicts(paths['information.xlsx'], sheet='forum', as_dict_list=True)
    if a is None:
        return a
    from collections import defaultdict
    dd = defaultdict(lambda: [])
    kk = list(a.keys())[0]
    for i, k in enumerate(kk.split(",")):
        k = k.replace("[", "")
        k = k.replace("]", "")
        k = k.split(" ")[0]
        for v in a[kk]:
            dd[k.lower()].append(v.split(",")[i])
    # list_dict2dict_list()
    # dd = dict_(dd)

    n = len(list(dd.values())[0])
    d2 = []
    for i in range(n):
        d2.append({k: v[i] for k, v in dd.items()})
    return d2

def class_information():
    course_number = core_conf['course_number']
    piazza = 'https://piazza.com/dtu.dk/%s%s/%s' % (semester().lower(), year(), course_number)
    paths = get_paths()
    teachers = xlsx_to_dicts(paths['information.xlsx'], sheet='teachers')
    students, all_groups = populate_student_report_results( get_enrolled_students() )
    continuing_education_mode = core_conf['continuing_education_mode']
    faq = xlsx_to_dicts(paths['information.xlsx'], sheet='faq')


    d = {'year': year(),
         'piazza': piazza, # deprecated.
         'course_number': course_number,
         'semester': semester(),
         'reports_handout': [1,6],
         'reports_handin': [6,11],
         'semester_id': semester_id(),
         'today': today(),
         'instructors': get_instructors(),
         'students': students,
         'teachers': teachers,
         "CE": continuing_education_mode,
         "all_groups": all_groups,
         "faq": faq,
         'forum': get_forum(paths),
         }

    written_exam = xlsx_to_dicts(paths['information.xlsx'], sheet='exam', as_dict_list=True)
    if "solution_q" in written_exam:
        written_exam['solution'] = {n:a for n,a in zip( written_exam['solution_q'], written_exam['solution_a'] ) }

    d['written_exam'] = written_exam

    gi = xlsx_to_dicts(paths['information.xlsx'], sheet='general_information', as_dict_list=True)
    for (k, v) in zip(gi['key'], gi['value']):
        if v == 'True':
            v = True
        if v == 'False':
            v= False
        gi[k] = v
    del gi['key']
    del gi['value']

    from thtools.coursebox.core.citations import get_references
    if "pensum_bib" in gi:
        refs, nrefs = get_references(paths['02450public'] + "/" + gi['pensum_bib'], gi)
        d['references'], d['new_references'] = refs, nrefs
    else:
        d['references'], d['new_references'] = None, None
    d.update(gi)
    # set first day of class if CE
    if continuing_education_mode:
        ice = xlsx_to_dicts(paths['information.xlsx'], sheet='ce', as_dict_list=True)
        d.update(ice)

    d['lectures'], d['references'] = lectures(info=d, pensum=d['references'])

    d['first_day_of_class'] = first_day_of_class(info=d)
    d['day_of_week_str'] = d['first_day_of_class'].strftime('%A')
    if "piazza" in gi:
        d['piazza'] = gi['piazza']

    for k in ['freeze_report_evaluation', 'freeze_grades']:
        freeze = gi[k]
        freeze = freeze == "True" if isinstance(freeze, str) else freeze
        freeze = freeze[0] if isinstance(freeze, list) else freeze
        gi[k] = freeze

    for k,v in core_conf.items():
        d[k] = v

    d['CE2'] = gi.get("days", 5) == 2 if continuing_education_mode else False
    d['CE5'] = gi.get("days", 5) == 5 if continuing_education_mode else False

    d['freeze_report_evaluation'] = d['freeze_report_evaluation'] == 'True'
    d['freeze_grades'] = d['freeze_grades'] == 'True'

    d['rooms'] = xlsx_to_dicts(paths['information.xlsx'], sheet='rooms')
    fix_instructor_comma(d['rooms'], d['instructors'])

    d['teams'] = xlsx_to_dicts(paths['information.xlsx'], sheet='teams')
    fix_instructor_comma(d['teams'], d['instructors'])
    return d

def fix_instructor_comma(dd, instructors):
    for r in dd:
        ri_shortnames = [i.strip().lower() for i in r['instructors'].split(",")]
        ri = []
        for sn in ri_shortnames:
            di = [i for i in instructors if i['shortname'] == sn ]
            if not di:
                print("Did not find shortname: " + sn + ". This seems bad.")
            ri += di
        r['instructors'] = ri