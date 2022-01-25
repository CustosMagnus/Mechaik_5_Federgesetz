import plotly.express as px
import pandas

def get_data(name): # extracts points from file
    ### var ###
    o = open(name, "r")
    # file names need to be data_feder.txt and data_gummi.txt, data must be formatted like the following:
    # weight; delta_s
    # weight; delta_s
    # ...
    txt = o.read()
    o.close()
    ### /var ###

    txt = txt.split("\n")
    if txt[-1] == "":
        txt.pop()
    for i in range(len(txt)):
        txt[i] = txt[i].split("; ")
    for i in range(len(txt)):
        for _ in range(2):
            txt[i][_] = float(txt[i][_])
    txt2 = []
    for i in range(len(txt)):
        txt2.append(txt[i][1])
    return txt2

def fit_line(result): # linear fit
    distance_f = []
    distance_g = []
    for i in range(len(result["feder_delta_s"])):
        distance_f.append(result["feder_delta_s"][i]-result["average increment Feder"][i])
        distance_g.append(result["gummi_delta_s"][i] - result["average increment Gummi"][i])
    idistance_f = sum(distance_f)/len(distance_f)
    idistance_g = sum(distance_g)/len(distance_g)
    for i in range(len(distance_f)):
        result["average increment Feder"][i] = result["average increment Feder"][i] + idistance_f
        result["average increment Gummi"][i] = result["average increment Gummi"][i] + idistance_g
    return result

def calculate(): # main function
    feder = get_data("data_feder.txt")
    gummi = get_data("data_gummi.txt")

    increment_feder = []
    increment_gummi = []
    result = {"gewicht": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
              "feder_delta_s": feder, "gummi_delta_s": gummi,
              "average increment Feder": [],
              "average increment Gummi": []}
    for i in range(len(result["gewicht"])):
        try:
            increment_feder.append((result["feder_delta_s"][i+1]-result["feder_delta_s"][i]))
            increment_gummi.append((result["gummi_delta_s"][i + 1] - result["gummi_delta_s"][i]))
        except IndexError:
            pass

    avg_incr_feder = sum(increment_feder)/len(increment_feder)
    avg_incr_gummi = sum(increment_gummi)/len(increment_gummi)

    for i in range(10):
        result["average increment Feder"].append(avg_incr_feder*i)
        result["average increment Gummi"].append(avg_incr_gummi*i)

    for i in range(10): # accuracy of best fit line
        result = fit_line(result)

    print(f"""increment Feder: {(result['average increment Feder'][-1]-result['average increment Feder'][0])/(result['gewicht'][-1]-result['gewicht'][0])}
increment Gummi: {(result['average increment Gummi'][-1]-result['average increment Gummi'][0])/(result['gewicht'][-1]-result['gewicht'][0])}""")
    result = pandas.DataFrame(result)

    fig = px.scatter({"gewicht (g)": [], "strecke (mm)": []}, x="gewicht (g)", y="strecke (mm)")
    fig.add_scatter(x=result["gewicht"], y = result["feder_delta_s"], name = "Feder")
    fig.add_scatter(x=result["gewicht"], y = result["gummi_delta_s"], name = "Gummi")
    fig.add_scatter(x=result["gewicht"], y=result["average increment Gummi"], name="linear fit Gummi")
    fig.add_scatter(x=result["gewicht"], y=result["average increment Feder"], name="linear fit Feder")

    fig.show()
    return result

if __name__ == '__main__':
    calculate()
