import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load dataset from CSV file
df = pd.read_csv('trainingset.csv', header=None, names=['srcip', 'sport', 'dstip', 'dsport', 'proto', 'total_fpackets', 'total_fvolume', 'total_bpackets', 'total_bvolume', 'min_fpktl', 'mean_fpktl', 'max_fpktl', 'std_fpktl', 'min_bpktl', 'mean_bpktl', 'max_bpktl', 'std_bpktl', 'min_fiat', 'mean_fiat', 'max_fiat', 'std_fiat', 'min_biat', 'mean_biat', 'max_biat', 'std_biat', 'duration', 'service', 'src_bytes', 'dst_bytes', 'label'])

# Drop unused features
df.drop(['srcip', 'sport', 'dstip', 'dsport', 'service'], axis=1, inplace=True)

# Convert categorical features to numerical
df['proto'] = pd.Categorical(df['proto'])
df['proto'] = df['proto'].cat.codes
df['label'] = pd.Categorical(df['label'])
df['label'] = df['label'].cat.codes

# Scale numerical features
scaler = StandardScaler()
df[['total_fpackets', 'total_fvolume', 'total_bpackets', 'total_bvolume', 'min_fpktl', 'mean_fpktl', 'max_fpktl', 'std_fpktl', 'min_bpktl', 'mean_bpktl', 'max_bpktl', 'std_bpktl', 'min_fiat', 'mean_fiat', 'max_fiat', 'std_fiat', 'min_biat', 'mean_biat', 'max_biat', 'std_biat', 'duration', 'src_bytes', 'dst_bytes']] = scaler.fit_transform(df[['total_fpackets', 'total_fvolume', 'total_bpackets', 'total_bvolume', 'min_fpktl', 'mean_fpktl', 'max_fpktl', 'std_fpktl', 'min_bpktl', 'mean_bpktl', 'max_bpktl', 'std_bpktl', 'min_fiat', 'mean_fiat', 'max_fiat', 'std_fiat', 'min_biat', 'mean_biat', 'max_biat', 'std_biat', 'duration', 'src_bytes', 'dst_bytes']])

# Split dataset into training and testing sets
from sklearn.model_selection import train_test_split

X = df.drop(['label'], axis=1)  # Features
y = df['label']  # Labels
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
