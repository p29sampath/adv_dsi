from sklearn.metrics import accuracy_score, confusion_matrix,roc_curve, roc_auc_score, precision_score, recall_score, precision_recall_curve, f1_score, plot_confusion_matrix
import matplotlib.pyplot as plt

def eval_model(classifier, X_train, y_train, X_val, y_val, show=True):
  '''
  classifier : Model to be evaluated
  X_train    : Features of training set
  y_train    : Target value of training set
  X_val      : Features of valuation set
  y_val      : Target valu of valuation set
  show       : Boolean - if the performance should be shown or not
  '''

  model = classifier.fit(X_train,y_train)
  roc_score_training = get_performance(model, X_train, y_train, "Train", show)
  roc_score_val = get_performance(model, X_val, y_val, "Validate", show)  

  return model, roc_score_training, roc_score_val

def get_performance(mod, xvar, yvar, runtype, show):
  '''
  mod     : Model to be evaluated
  xvar    : Feature columns usually x_train/x_test/x_val
  yvar    : Target Column corresponding y_train/y_test/y_val
  runtype : Hardcoded value to indicate run type Train/Test/Validate. This gets printed at the end of score and as title for confusion matrix
  show    : Boolean - if the performance should be shown or not
	
  Extension Scope 
  - Add more relavent scores 
  - Have a switch to select / remove metrics
  - More Plots/Graphs for clear indications
  '''
  mod_pred = mod.predict(xvar)
  mod_pred_proba = mod.predict_proba(xvar)[:, 1]

  mod_roc_score = roc_auc_score(yvar, mod_pred_proba)
  
  if show:
    print('Accuracy Score: ',accuracy_score(yvar,mod_pred),' F1 Score ',f1_score(yvar,mod_pred),' Precision Score ', precision_score(yvar,mod_pred),' Recall Score ', recall_score(yvar,mod_pred), ' R2 Score ',mod.score(xvar, yvar),' ROC_AUC_SCORE ', mod_roc_score,'(',runtype,')')
    disp = plot_confusion_matrix(mod, xvar, yvar, cmap=plt.cm.Blues)
    disp.ax_.set_title('Confusion Matrix '+runtype)
  
  return mod_roc_score
