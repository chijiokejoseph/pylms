from pylms.constants import NAME
from pylms.data_service import load
from pylms.record import RecordStatus

ds = load().unwrap()

pretty = ds.to_pretty()

data = ds.as_ref()

date = "07/01/2026"
data.loc[data.index[[10, 53, 21, 95, 49, 17, 47, 63, 70, 72, 43, 80, 56]], date] = str(
    RecordStatus.PRESENT
)

data[date] = data[date].astype(str)

data[date].replace("nan", "Absent", inplace=True)


print(f"{data.loc[0:49, date] = }")
