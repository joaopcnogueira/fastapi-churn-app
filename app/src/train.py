import joblib
import pandas as pd
from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from feature_engine.encoding import OneHotEncoder

BASE_DIR = Path('.')
df = pd.read_csv(BASE_DIR/'datasets/abt_churn.csv')

num_vars = ['tot_orders_12m', 'tot_items_12m', 'tot_items_dist_12m', 'receita_12m', 'recencia']
cat_vars = ['uf']
target = 'churn_next_6m'
features = cat_vars + num_vars

X = df[features].copy()
y = df[target]

model = Pipeline(steps=[
        ('OHE', OneHotEncoder(variables=cat_vars, drop_last=True)),
        ('ALGO', RandomForestClassifier(random_state=30))
    ]
)

model.fit(X, y)

model_artefacts = {
    'num_vars': num_vars, 
    'cat_vars': cat_vars, 
    'features': features,
    'target': target, 
    'model': model
}

joblib.dump(model_artefacts, BASE_DIR/'pkls/model.pkl')
