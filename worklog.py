import pandas

def main():
    worklog = pandas.read_csv('./worklog.csv')
    worklog.subproject.fillna('unknown', inplace=True)
    hours_by_sub = worklog.groupby('subproject').hours.sum(axis='rows')
    print(hours_by_sub)

if __name__ == '__main__':
    main()
