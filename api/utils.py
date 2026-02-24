import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression

def train_and_save_model(csv_path='StudentPerformanceFactors.csv', model_path='best_linear_model.pkl'):
    print("Training model from scratch to ensure compatibility...")
    df = pd.read_csv(csv_path)
    
    # Handle missing values as done in the notebook (using mode)
    for col in ['Teacher_Quality', 'Parental_Education_Level', 'Distance_from_Home']:
        df[col] = df[col].fillna(df[col].mode()[0])

    categorical_features = [
        'Parental_Involvement', 'Access_to_Resources', 'Extracurricular_Activities',
        'Motivation_Level', 'Internet_Access', 'Family_Income', 'Teacher_Quality',
        'School_Type', 'Peer_Influence', 'Learning_Disabilities',
        'Parental_Education_Level', 'Distance_from_Home', 'Gender'
    ]
    numerical_features = [
        'Hours_Studied', 'Attendance', 'Sleep_Hours', 
        'Previous_Scores', 'Tutoring_Sessions', 'Physical_Activity'
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ]
    )

    X = df.drop('Exam_Score', axis=1)
    y = df['Exam_Score']

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])

    model.fit(X, y)
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    return model

if __name__ == "__main__":
    train_and_save_model()
