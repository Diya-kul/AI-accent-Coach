# TEST THE MODEL 
test_file= "sample.ogg"

features= extract_features(test_file)
prediction= model.predict([features])

if prediction[0] == 0:
    print("Indian accent")
elif prediction[0]==1:
    print("British accent")
else:
    print("American accent")