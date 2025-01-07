from dotenv import load_dotenv

load_dotenv()

class AccidentCategorizer:
    
    #근속년수 카테고리화
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
            return 1
        elif service_year in two :
            return 2
        elif service_year in three :
            return 3
        elif service_year in four :
            return 4
        elif service_year in five :
            return 5
        elif service_year in six :
            return 6
        elif service_year in seven :
            return 7
        else:
            return 8
        
    #공사규모 카테고리화
    @staticmethod
    def categorize_scale_text(scale) :
        two = ["100인~299인","100인~499인"]
        three = ["10인~99인","50인~99인"]
        four = ["9인~50인"]
        if scale in two :
            return 2
        elif scale in three :
            return 3
        elif scale in four :
            return 4
        else :
            return 1
        
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
            return 2
        elif 50 <= scale < 100 :
            return 3
        elif 100 <= scale < 500 :
            return 4
        else :
            return 1
        
    @staticmethod
    def categorize_time_range(time) :
        if 0 <= time < 2:
            return 5
        elif 2 <= time < 4:
            return 1
        elif 4 <= time < 6:
            return 3
        elif 6 <= time < 8:
            return 7
        elif 8 <= time < 10:
            return 11
        elif 10 <= time < 12:
            return 12
        elif 12 <= time < 14:
            return 9
        elif 14 <= time < 16:
            return 10
        elif 16 <= time < 18:
            return 8
        elif 18 <= time < 20:
            return 6
        elif 20 <= time < 22:
            return 2
        return 4
