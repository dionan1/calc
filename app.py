from flask import Flask, request, render_template

app = Flask(__name__)

# Function to calculate grades
def calculate_grades(prelim):
    prelim_weight = 0.2
    midterm_weight = 0.3
    final_weight = 0.5
    desired_grade = 75

    prelim_score = float(prelim) * prelim_weight
    added_weights = midterm_weight + final_weight
    required_midterm_final = (desired_grade - prelim_score) / added_weights

    if required_midterm_final > 100:
        return None, None, True, False, False
    else:
        midterm_final_grade = round(required_midterm_final, 2)
        dean_list = midterm_final_grade <= 81.25
        difficult_pass = midterm_final_grade >= 90
        return midterm_final_grade, midterm_final_grade, False, dean_list, difficult_pass

@app.route('/', methods=['GET', 'POST'])
def index():
    prelim = ""
    midterm = ""
    final = ""
    error = ""
    impossible = False
    dean_list = False
    difficult_pass = False

    if request.method == 'POST':
        prelim = request.form['prelim']
        try:
            prelim = float(prelim)
            if prelim < 1 or prelim > 100:
                error = "Please enter a grade between 1 and 100."
            else:
                midterm, final, impossible, dean_list, difficult_pass = calculate_grades(prelim)
                if impossible:
                    error = "It is impossible to achieve the desired grade with the given prelim score."
        except ValueError:
            error = "Invalid input. Please enter a valid number."

    return render_template('index.html', prelim=prelim, midterm=midterm, final=final, error=error, dean_list=dean_list, difficult_pass=difficult_pass)

if __name__ == "__main__":
    app.run(debug=True)