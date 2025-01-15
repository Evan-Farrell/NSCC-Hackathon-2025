


def gen_course():
    course={"name": 'widgets 101',
            "code": 'W1000',
            "unit_value":1,
            "misc":"could add anything else you need..."
            }
    return course

course_list_A=[]
course_list_B=[]
for x in range(0,6):
    course_list_A.append(gen_course())
    course_list_B.append(gen_course())

term1={"term_session":"Fall 2019",
       "course_list":course_list_A
      }

term2={"term_session":"Winter 2020",
       "course_list":course_list_B
      }


remaining_courses=[term1,term2]


student_info={
    'id':"W0518150",
    'name':"Evan Farrell",
    'program': 'iot blah blah',
    'on_track': 1, #true if the student is behind the road map 'i.e bad student'
    'terms_left': 2, #shortest number of terms left to graduate
    'progress_roadmap': "some image file.png",
    'remaining_courses':remaining_courses
}

#print(student_info['remaining_courses'][1]["course_list"][5]['code'])
print(student_info)