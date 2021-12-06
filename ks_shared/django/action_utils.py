import pandas as pd
import io
from datetime import datetime
from django.http import HttpResponse


def generate_excel(self, col, filename):
    qs = self.filter_queryset(self.get_queryset())
    serializer = self.get_serializer(qs, many=True)
    dataframe = pd.DataFrame(serializer.data, columns=col)
    output = io.BytesIO()
    dataframe.to_excel(output, index=False)
    response = HttpResponse()
    response["Content-Type"] = "application/vnd.ms-excel"
    file_name = '{}_{}.xlsx'.format(filename, datetime.today())
    response['Content-Disposition'] = 'attachment;filename={}'.format(file_name)
    response.write(output.getvalue())
    output.close()
    return response
