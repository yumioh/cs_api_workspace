from dotenv import load_dotenv

load_dotenv()

class AccidentCategorizer:

    #재해율이 높은 순서로 카테고리화 : 재해수가 많을수록 높은 점수
    
    #근속년수 카테고리화
    @staticmethod
    # def categrize_service_year(service_year) :
    #     one = ["1개월미만","1개월~2개월미만","3개월~4개월미만","4개월~5개월미만","6개월미만"]
    #     two = ["6개월~1년"]
    #     three  = ["1~2년","1년~2년미만"]
    #     four = ["2~3년","2년~3년미만"]
    #     five = ["3~4년","3년~4년미만"]
    #     six = ["4~5년","4년~5년"]
    #     seven = ["5~10년","5년~10년"]

    #     service_year = service_year.replace(" ", "")

    #     if service_year in one :
    #         return 1
    #     elif service_year in two :
    #         return 2
    #     elif service_year in three :
    #         return 3
    #     elif service_year in four :
    #         return 4
    #     elif service_year in five :
    #         return 5
    #     elif service_year in six :
    #         return 6
    #     elif service_year in seven :
    #         return 7
    #     else:
    #         return 8
        
    @staticmethod
    def categrize_service_year(service_year) :
        one = ["1개월미만","1개월~2개월미만","3개월~4개월미만","4개월~5개월미만","6개월미만"]
        two = ["6개월~1년"]
        three  = ["1~2년","1년~2년미만"]
        four = ["2~3년","2년~3년미만"]
        five = ["3~4년","3년~4년미만"]
        six = ["4~5년","4년~5년"]
        seven = ["5~10년","5년~10년"]

        service_year = service_year.replace(" ", "")

        if service_year in one :
            return 8 
        elif service_year in two :
            return 5
        elif service_year in three :
            return 6
        elif service_year in four :
            return 3
        elif service_year in five :
            return 2
        elif service_year in six :
            return 1
        elif service_year in seven :
            return 4
        else :
            return 7
        
    #공사규모 카테고리화
    @staticmethod
    def categorize_scale_kosha(scale) :
        if scale in "소소" :
            return 5
        elif scale in "소" :
            return 4
        elif scale in "중" :
            return 3
        elif scale in "대" :
            return 2
        else :
            return 1
    
    #공사규모 카테고리화 
    @staticmethod
    def categorize_scale_number(scale) :
        if 9 <= scale < 50:
            return 4
        elif 50 <= scale < 100 :
            return 3
        elif 100 <= scale < 500 :
            return 2
        elif scale <= 500 :
            return 1
        else :
            return 5
    
    #근무시간별 카테고리화
    @staticmethod
    def categorize_time_range(time) :
        if 0 <= time < 2:
            return 6
        elif 2 <= time < 4:
            return 1
        elif 4 <= time < 6:
            return 3
        elif 6 <= time < 8:
            return 7
        elif 8 <= time < 10:
            return 10
        elif 10 <= time < 12:
            return 12
        elif 12 <= time < 14:
            return 9
        elif 14 <= time < 16:
            return 11
        elif 16 <= time < 18:
            return 8
        elif 18 <= time < 20:
            return 5
        elif 20 <= time < 22:
            return 4
        return 2
    
    #나이 카테고리화
    @staticmethod
    def categorize_age_num(age) :
        if 10 <= age < 20 :
            return 2
        elif 20 <= age < 30 :
            return 3
        elif 30 <= age < 40 :
            return 4
        elif 40 <= age < 50 :
            return 5
        elif 50 <= age < 60 :
            return 6
        elif 60 <= age < 70 :
            return 7
        elif 70 <= age < 80 :
            return 8
        else :
            return 1
