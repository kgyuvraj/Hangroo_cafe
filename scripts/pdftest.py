import pandas as pd
import jinja2

interest_rates = [i*.01 for i in range(1,11)]
initial_account_sizes = [100, 500, 20000, 50000]
data_frames = []
for interest_rate in interest_rates:
    df = {}
    for initial_account_size in initial_account_sizes:
        df['Account Size: ' + str(initial_account_size)] = [initial_account_size * (1 + interest_rate) ** year for year in range(1, 21)]
    df = pd.DataFrame(df)
    df.index.name = 'year'
    data_frames.append({'df':df,
        'interest_rate':interest_rate})


templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "pdftemplate.html"
template = templateEnv.get_template(TEMPLATE_FILE)


for d in data_frames:
    outputText = template.render(df=d['df'],interest_rate=d['interest_rate'])
    html_file = open(str(int(d['interest_rate'] * 100)) + '.html', 'w')
    html_file.write(outputText)
    html_file.close()


import pdfkit
for i in range(1,11):
    pdfkit.from_file(str(i) + '.html', str(i) + '.pdf')