import numpy as np
from numpy.typing import NDArray
from typing import Any

"""
   In the first two set of tasks, we will narrowly focus on accuracy - 
   what fraction of our predictions were correct. However, there are several 
   popular evaluation metrics. You will learn how (and when) to use these evaluation metrics.
"""


# ======================================================================
class Section3:
    def __init__(
        self,
        normalize: bool = True,
        frac_train=0.2,
        seed=42,
    ):
        self.seed = seed
        self.normalize = normalize

    def analyze_class_distribution(self, y: NDArray[np.int32]) -> dict[str, Any]:
        """
        Analyzes and prints the class distribution in the dataset.

        Parameters:
        - y (array-like): Labels dataset.

        Returns:
        - dict: A dictionary containing the count of elements in each class and the total number of classes.
        """
        # Your code here to analyze class distribution
        # Hint: Consider using collections.Counter or numpy.unique for counting

        uniq, counts = np.unique(y, return_counts=True)
        print(f"{uniq=}")
        print(f"{counts=}")
        print(f"{np.sum(counts)=}")
        class_counts = dict(zip(uniq, counts))
        return {
            "class_counts": class_counts,  # Replace with actual class counts
            "num_classes": len(uniq),  # Replace with the actual number of classes
        }

    # --------------------------------------------------------------------------
    """
    A. Using the same classifier and hyperparameters as the one used at the end of part 2.B. 
       Get the accuracies of the training/test set scores using the top_k_accuracy score for k=1,2,3,4,5. 
       Make a plot of k vs. score for both training and testing data and comment on the rate of accuracy change. 
       Do you think this metric is useful for this dataset?
    """

    def partA(
        self,
        Xtrain: NDArray[np.floating],
        ytrain: NDArray[np.int32],
        Xtest: NDArray[np.floating],
        ytest: NDArray[np.int32],
    ) -> tuple[
        dict[Any, Any],
        NDArray[np.floating],
        NDArray[np.int32],
        NDArray[np.floating],
        NDArray[np.int32],
    ]:
        """ """
        # Enter code and return the `answer`` dictionary

        answer = {}

        """
        # `answer` is a dictionary with the following keys:
        - integers for each topk (1,2,3,4,5)
        - "clf" : the classifier
        - "plot_k_vs_score_train" : the plot of k vs. score for the training data, 
                                    a list of tuples (k, score) for k=1,2,3,4,5
        - "plot_k_vs_score_test" : the plot of k vs. score for the testing data
                                    a list of tuples (k, score) for k=1,2,3,4,5

        # Comment on the rate of accuracy change for testing data
        - "text_rate_accuracy_change" : the rate of accuracy change for the testing data

        # Comment on the rate of accuracy change
        - "text_is_topk_useful_and_why" : provide a description as a string

        answer[k] (k=1,2,3,4,5) is a dictionary with the following keys: 
        - "score_train" : the topk accuracy score for the training set
        - "score_test" : the topk accuracy score for the testing set
        """
        clf = LogisticRegression(max_iter=300) 
        clf.fit(Xtrain, ytrain)  

        k_values = [1, 2, 3, 4, 5]

        answer = {}

        scores_train = []
        scores_test = []

        scores_train = [top_k_accuracy_score(ytrain, clf.predict_proba(Xtrain), k=i) for i in k_values]
        scores_test = [top_k_accuracy_score(ytest, clf.predict_proba(Xtest), k=i) for i in k_values]

        for j, l in enumerate(k_values):
            answer[l] = {"score_train": scores_train[j], "score_test": scores_test[j]}
       answer.update({
            "clf": clf,
            "plot_k_vs_score_train": list(zip(k_values, scores_train)),
            "plot_k_vs_score_test": list(zip(k_values, scores_test)),
            "text_rate_accuracy_change": "With the increase in k, top-k accuracy typically rises due to the model having more opportunities to encompass the correct class within its top k predictions. However, as k continues to grow, the incremental gains in accuracy tend to taper off",
            "text_is_topk_useful_and_why": "Top-k accuracy is valuable for situations where the precise ranking of the correct category is less critical than ensuring the correct category appears within the top k selections. This metric is especially pertinent to multi-class classification challenges involving numerous categories or scenarios where an approximate prediction holds significance"   })

        
        return answer, Xtrain, ytrain, Xtest, ytest

    # --------------------------------------------------------------------------
    """
    B. Repeat part 1.B but return an imbalanced dataset consisting of 90% of all 9s removed.  Also convert the 7s to 0s and 9s to 1s.
    """

    def partB(
        self,
        X: NDArray[np.floating],
        y: NDArray[np.int32],
        Xtest: NDArray[np.floating],
        ytest: NDArray[np.int32],
    ) -> tuple[
        dict[Any, Any],
        NDArray[np.floating],
        NDArray[np.int32],
        NDArray[np.floating],
        NDArray[np.int32],
    ]:
        """"""
        # Enter your code and fill the `answer` dictionary
        answer = {}
        X, y = nu.filter_imbal_7_9s(X, y)
        Xtest, ytest = nu.filter_imbal_7_9s(Xtest, ytest)
        test_Xtrain = nu.scalex(X)
        test_Xtest = nu.scalex(Xtest)
        test_ytrain = nu.scaley(y)
        test_ytest = nu.scaley(ytest)
        print("Xtrain elements scaled  " +str(test_Xtrain))
        print("Xtest elements scaled  " +str(test_Xtest))
        print("ytrain elements represented as  " +str(test_ytrain))
        print("ytest elements represented as  " +str(test_ytest))
        answer = {}

        length_Xtrain = len(X)
        length_Xtest = len(Xtest)
        length_ytrain = len(y)
        length_ytest = len(ytest)
        max_Xtrain = X.max()
        max_Xtest = Xtest.max()
        print(f" {length_Xtrain}, {length_Xtest}, {length_ytrain}, {length_ytest}")
        print(f" {max_Xtrain}, {max_Xtest}")
        answer["length_Xtrain"] = length_Xtrain 
        answer["length_Xtest"] = length_Xtest
        answer["length_ytrain"] = length_ytrain
        answer["length_ytest"] = length_ytest
        answer["max_Xtrain"] = max_Xtrain
        answer["max_Xtest"] = max_Xtest
        # Answer is a dictionary with the same keys as part 1.B
      
        return answer, X, y, Xtest, ytest

    # --------------------------------------------------------------------------
    """
    C. Repeat part 1.C for this dataset but use a support vector machine (SVC in sklearn). 
        Make sure to use a stratified cross-validation strategy. In addition to regular accuracy 
        also print out the mean/std of the F1 score, precision, and recall. As usual, use 5 splits. 
        Is precision or recall higher? Explain. Finally, train the classifier on all the training data 
        and plot the confusion matrix.
        Hint: use the make_scorer function with the average='macro' argument for a multiclass dataset. 
    """

    def partC(
        self,
        X: NDArray[np.floating],
        y: NDArray[np.int32],
        Xtest: NDArray[np.floating],
        ytest: NDArray[np.int32],
    ) -> dict[str, Any]:
        """"""
        Xtrain, ytrain = X, y
        Xtest, ytest = Xtest, ytest

        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=52)
        svc_clf = SVC(random_state=52)
       scoring = {
        'accuracy': 'accuracy',
        'f1_score': make_scorer(f1_score, average='macro'),
        'precision': make_scorer(precision_score, average='macro'),
        'recall': make_scorer(recall_score, average='macro')
        }

        scores = cross_validate(svc_clf, Xtrain, ytrain, scoring=scoring, cv=skf, return_train_score=False)

        scores_3C = {
        'mean_accuracy': np.mean(scores['test_accuracy']),
        'std_accuracy': np.std(scores['test_accuracy']),
        'mean_f1': np.mean(scores['test_f1_score']),
        'std_f1': np.std(scores['test_f1_score']),
        'mean_precision': np.mean(scores['test_precision']),
        'std_precision': np.std(scores['test_precision']),
        'mean_recall': np.mean(scores['test_recall']),
        'std_recall': np.std(scores['test_recall'])
        }
        svc_clf.fit(Xtrain, ytrain)
        train_y_pred = svc_clf.predict(Xtrain)
        train_confusion_matrix = confusion_matrix(ytrain, train_y_pred)
        test_y_pred = svc_clf.predict(Xtest)
        test_confusion_matrix = confusion_matrix(ytest, test_y_pred)
        
        # Enter your code and fill the `answer` dictionary
        answer = {
            'scores': scores_3C,
            'cv': skf,
            'clf': svc_clf,
            'confusion_matrix_train': train_confusion_matrix,
            'confusion_matrix_test': test_confusion_matrix
        }

        """
        Answer is a dictionary with the following keys: 
        - "scores" : a dictionary with the mean/std of the F1 score, precision, and recall
        - "cv" : the cross-validation strategy
        - "clf" : the classifier
        - "is_precision_higher_than_recall" : a boolean
        - "explain_is_precision_higher_than_recall" : a string
        - "confusion_matrix_train" : the confusion matrix for the training set
        - "confusion_matrix_test" : the confusion matrix for the testing set
        
        answer["scores"] is dictionary with the following keys, generated from the cross-validator:
        - "mean_accuracy" : the mean accuracy
        - "mean_recall" : the mean recall
        - "mean_precision" : the mean precision
        - "mean_f1" : the mean f1
        - "std_accuracy" : the std accuracy
        - "std_recall" : the std recall
        - "std_precision" : the std precision
        - "std_f1" : the std f1
        """
       precision_higher_than_recall = answer['scores']['mean_precision'] > answer['scores']['mean_recall']
       answer['is_precision_higher_than_recall'] = precision_higher_than_recall
       answer['explain_is_precision_higher_than_recall'] = "Out of all positive predictions, the model reliably identifies true positive cases with a higher degree of precision than recall. In datasets with an unequal class distribution, this situation frequently arises, where the model does better at minimizing false negatives than false positives. In essence, the model does a better job of guaranteeing the accuracy of its positive predictions than it does at collecting all real positives."
      
        return answer

    # --------------------------------------------------------------------------
    """
    D. Repeat the same steps as part 3.C but apply a weighted loss function (see the class_weights parameter).  Print out the class weights, and comment on the performance difference. Use the `compute_class_weight` argument of the estimator to compute the class weights. 
    """

    def partD(
        self,
        X: NDArray[np.floating],
        y: NDArray[np.int32],
        Xtest: NDArray[np.floating],
        ytest: NDArray[np.int32],
    ) -> dict[str, Any]:
        """"""
        # Enter your code and fill the `answer` dictionary
        answer = {}
        Xtrain, ytrain = X, y
        Xtest, ytest = Xtest, ytest
    
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=52)
        scoring = {
        'accuracy': 'accuracy',
        'f1_score': make_scorer(f1_score, average='macro'),
        'precision': make_scorer(precision_score, average='macro'),
        'recall': make_scorer(recall_score, average='macro')
        }
        class_weights = compute_class_weight(class_weight='balanced', classes=np.unique(ytrain), y=ytrain)
        class_weights_dict = {0: class_weights[0], 1: class_weights[1]}
        svc_clf_weighted = SVC(random_state=52, class_weight=class_weights_dict)
        scores = cross_validate(svc_clf_weighted, Xtrain, ytrain, scoring=scoring, cv=skf, return_train_score=False)
        scores_3D = {metric: {'mean': np.mean(scores[f'test_{metric}']), 'std': np.std(scores[f'test_{metric}'])} 
                    for metric in ['accuracy', 'f1_score', 'precision', 'recall']}
        svc_clf_weighted.fit(Xtrain, ytrain)
        train_conf_mat_weighted = confusion_matrix(ytrain, svc_clf_weighted.predict(Xtrain))
        test_conf_mat_weighted = confusion_matrix(ytest, svc_clf_weighted.predict(Xtest))
        answer = {
            'scores': scores_3D,
            'cv': skf,
            'clf': svc_clf_weighted,
            'class_weights': class_weights_dict,
            'confusion_matrix_train': train_conf_mat_weighted,
            'confusion_matrix_test': test_conf_mat_weighted,
            'explain_purpose_of_class_weights': "Class weights are used to give more importance to underrepresented classes during the training of the classifier. This helps to mitigate the bias towards the majority class in imbalanced datasets and aims to improve the classifier's performance on the minority class",
            'explain_performance_difference': "Using class weights may improve recall for the minority class at the expense of precision, as the classifier is encouraged to correctly classify the minority class instances, potentially increasing the false positives"
        }

       
        """
        Answer is a dictionary with the following keys: 
        - "scores" : a dictionary with the mean/std of the F1 score, precision, and recall
        - "cv" : the cross-validation strategy
        - "clf" : the classifier
        - "class_weights" : the class weights
        - "confusion_matrix_train" : the confusion matrix for the training set
        - "confusion_matrix_test" : the confusion matrix for the testing set
        - "explain_purpose_of_class_weights" : explanatory string
        - "explain_performance_difference" : explanatory string

        answer["scores"] has the following keys: 
        - "mean_accuracy" : the mean accuracy
        - "mean_recall" : the mean recall
        - "mean_precision" : the mean precision
        - "mean_f1" : the mean f1
        - "std_accuracy" : the std accuracy
        - "std_recall" : the std recall
        - "std_precision" : the std precision
        - "std_f1" : the std f1

        Recall: The scores are based on the results of the cross-validation step
        """
      
        return answer
