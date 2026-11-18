AI-BASED SMART SHOPPING ASSISTANT USING SVM, VADER SENTIMENT ANALYSIS FOR INTELLIGENT PRODUCT RECOMMENDATION

A PROJECT REPORT (PHASE - 1)

Submitted by

SWETHA S	(731623201057)
SREEJA M	(731623201054)
VISHAL S	(731623201062)

in partial fulfillment for the award of the degree
of
BACHELOR OF ENGINEERING
in
INFORMATION TECHNOLOGY

K S R INSTITUTE FOR ENGINEERING AND TECHNOLOGY
(Autonomous)
TIRUCHENGODE – 637 215

ANNA UNIVERSITY :: CHENNAI 600 025

NOVEMBER 2026

K S R INSTITUTE FOR ENGINEERING AND TECHNOLOGY
(Autonomous)
TIRUCHENGODE – 637215

ANNA UNIVERSITY :: CHENNAI 600 025


# BONAFIDE CERTIFICATE

Certified that this project report "AI-BASED SMART SHOPPING ASSISTANT USING SVM, VADER SENTIMENT ANALYSIS FOR INTELLIGENT PRODUCT RECOMMENDATION" is the Bonafide work of SWETHA S (731623201057), SREEJA M (731623201054) and VISHAL S (731623201062) who carried out the project work under my supervision.

SIGNATURE OF THE SUPERVISOR			SIGNATURE OF THE HOD
Dr. S. ANGURAJ, M.E., Ph.D.,			Dr. S. ANGURAJ, M.E., Ph.D.,
Associate Professor & Head,				Associate Professor & Head,
Department of IT,					Department of IT,
K.S.R College of Engineering,				K.S.R College of Engineering,
Tiruchengode – 637215.				Tiruchengode – 637215.

Submitted for the Project Viva Voce examination held on ………………………

**Internal Examiner					External Examiner**


# ACKNOWLEDGEMENT

We wish to express our sincere thanks behind every achievement lies an unfathomable sea of gratitude to those who actuated it, without them it would never have existed.

We wish our heartfelt thanks to our respected Founder of K S R Educational Institutions Theivathiru Lion Dr. K. S. Rangasamy MJF., and to the Chairman Mr. R. Srinivasan BBM., of K S R Educational Institutions for their moral support throughout the project.

We wish our sincere thanks to respected Dean Dr. M. Venkatesan, M.E., Ph.D., for allowing us to have the extensive use of college facilities to do this project effectively.

We would like to extend our heartfelt gratitude to our esteemed principal, Dr. P. Meenakshi Devi, M.E., Ph.D., for inspiring us to carry out the project successfully.

We would like to express our sincere gratitude to our respected Head of Department Dr. S. Anguraj, M.E., Ph.D., for his valuable guidance and constant motivation.

We wish to express our sincere thanks to our Guide Dr. S. Anguraj, M.E., Ph.D., for the continuous help over the period and the creation of ideas for this phase of project work. We would like to extend our warmest thanks to all our parents and friends for their enduring support.

**Sreeja M				Swetha S				Vishal S**


# ABSTRACT

The aim of this project is to help online shoppers choose the best product and the best store with confidence. Existing recommendation systems rely mainly on star ratings and raw review text, assume that every review is genuine, and rarely combine review quality with live prices from more than one store, so shoppers can be misled by fake reviews and higher prices. The proposed Intelligent Product Recommendation system collects product prices and customer reviews from Indian e-commerce websites using Playwright-based scrapers and stores them in a MySQL database. In baseline experiments, SVM and VADER were evaluated, while in the primary deployment, review sentiment is computed with TextBlob polarity, and fake reviews are detected using TF-IDF features and a Random Forest classifier trained on 40,432 labelled reviews.

The system derives a Price Score, a Sentiment Score and a Trust Score and combines them with weights of 0.40, 0.30 and 0.30 into a Value Score that drives a BUY NOW, CONSIDER or WAIT decision. The main modules are web scraping, sentiment analysis, fake review detection, score computation, recommendation and festival offer analysis, delivered through a FastAPI backend and a web interface. The fake review model achieved an accuracy of 84.27%, a precision of 82.44%, a recall of 87.09% and an F1-score of 84.70% on a stratified 20% test set. In this phase the architectural design, literature survey, and baseline modules are completed.

Keywords: Product recommendation, Sentiment analysis, Fake review detection, Random Forest, TF-IDF, SVM, VADER, Price comparison, E-commerce


# TABLE OF CONTENTS


| CHAPTER NO. | TITLE | PAGE NO. |
| --- | --- | --- |
|  | ACKNOWLEDGEMENT | iii |
|  | ABSTRACT | iv |
|  | LIST OF TABLES | vi |
|  | LIST OF FIGURES | vii |
|  | LIST OF ABBREVIATIONS | viii |
| 1 | INTRODUCTION | 1 |
|  | 1.1 General | 1 |
|  | 1.2 Background of the Study | 2 |
|  | 1.3 Problem Statement | 3 |
|  | 1.4 Aim of the Project | 4 |
|  | 1.5 Objectives of the Project | 4 |
|  | 1.6 Scope and Organization of the Report | 5 |
| 2 | LITERATURE SURVEY | 6 |
|  | 2.1 General | 6 |
|  | 2.2 Review of Literature | 7 |
|  | 2.2.1 Base Paper and Spam-Aware Recommendation | 7 |
|  | 2.2.2 Sentiment-Based and Hybrid Recommender Systems | 8 |
|  | 2.2.3 Sentiment Classification and Aspect-Level Analysis | 10 |
|  | 2.2.4 Fake Review Detection | 12 |
|  | 2.2.5 Review Credibility | 13 |
|  | 2.2.6 Price-Aware Recommendation | 14 |
|  | 2.3 Comparative Summary Table of Literature Survey | 15 |
|  | 2.4 Research Gap | 17 |
| 3 | CONVENTIONAL SYSTEM | 19 |
|  | 3.1 General | 19 |
|  | 3.2 Architecture and Working of Conventional Systems | 20 |
|  | 3.3 Methodologies and Algorithms Used in Existing Systems | 21 |
|  | 3.4 Analysis of the Base Paper | 22 |
|  | 3.5 Drawbacks of Existing Systems | 23 |
| 4 | PROPOSED SYSTEM | 24 |
|  | 4.1 General and Proposed System Architecture | 24 |
|  | 4.2 Module Description | 25 |
|  | 4.3 Mathematical Formulation and Scoring Logic | 26 |
|  | 4.4 System Flow Chart and Decision Heuristics | 27 |
|  | 4.5 Advantages and Comparison with Existing System | 28 |
| 5 | CONCLUSION AND FUTURE SCOPE | 29 |
|  | 5.1 Conclusion | 29 |
|  | 5.2 Future Scope | 29 |
|  | REFERENCES | 30 |


# LIST OF TABLES


| TABLE NO. | TITLE | PAGE NO. |
| --- | --- | --- |
| Table 2.1 | Comparative Summary Table of Selected Key Literature | 15 |
| Table 3.1 | Algorithms Used in Conventional Systems and Their Practical Limitations | 21 |
| Table 4.1 | Illustrative Value Score Calculation for Benchmark Product | 26 |
| Table 4.2 | Feature Comparison between Conventional System and Proposed System | 28 |


# LIST OF FIGURES


| FIGURE NO. | TITLE | PAGE NO. |
| --- | --- | --- |
| Fig. 4.1 | System Architecture of the Intelligent Product Recommendation System | 24 |
| Fig. 4.2 | Flow Chart of the Intelligent Product Recommendation System | 27 |


# LIST OF ABBREVIATIONS


| TERM | FULL FORM |
| --- | --- |
| AI | Artificial Intelligence |
| ML | Machine Learning |
| NLP | Natural Language Processing |
| TF-IDF | Term Frequency - Inverse Document Frequency |
| RF | Random Forest Classifier |
| SVM | Support Vector Machine |
| VADER | Valence Aware Dictionary and sEntiment Reasoner |
| CG | Computer-Generated (Synthetic Fake Review) |
| OR | Original / Organic Review (Genuine) |
| MCDM | Multi-Criteria Decision Making |
| API | Application Programming Interface |
| REST | Representational State Transfer |
| JSON | JavaScript Object Notation |
| DOM | Document Object Model |
| HTML | HyperText Markup Language |
| CSS | Cascading Style Sheets |
| BERT | Bidirectional Encoder Representations from Transformers |
| LSTM | Long Short-Term Memory |
| CNN | Convolutional Neural Network |
| ORM | Object Relational Mapping |
| SQL | Structured Query Language |
| UI/UX | User Interface / User Experience |


# CHAPTER 1

**INTRODUCTION**


## 1.1 GENERAL

Electronic commerce has become a routine part of daily life, and customer reviews have become one of the most important inputs for a purchase decision [1], [2]. Before buying a product online, a shopper normally compares its price on several websites, reads a few reviews and looks at the average star rating. This process is slow, and the shopper has little means of knowing whether the reviews are honest or whether the lowest price is also the best deal.

The people most affected are everyday online buyers, especially in markets such as India where the same product is listed on Amazon, Flipkart and other stores with different prices and frequent festival discounts. Fake and promotional reviews make the problem worse, because they reduce consumer trust and distort the evaluation of products [3], [4], [5]. Price is also an essential element that influences purchase behaviour [6], so a recommendation that ignores price is incomplete.

Most existing recommenders rely on ratings or on sentiment extracted from reviews and assume that every review is genuine, while only a few of them combine review credibility with price information [7], [8]. This project, Intelligent Product Recommendation using Sentiment Analysis, Fake Review Detection and Multi-Store Price Intelligence, is a web-based decision-support system. It collects the prices and customer reviews of a product from different online stores, measures the sentiment of the reviews, estimates how trustworthy the reviews are with a machine learning classifier, and combines these with the price into a single Value Score. The score is used to recommend the best store and to tell the shopper whether to buy now, consider the product or wait.


## 1.2 BACKGROUND OF THE STUDY

Sentiment analysis is the task of finding whether a piece of text expresses a positive, negative or neutral opinion. In lexicon-based tools such as TextBlob and VADER, words carry polarity values and the polarity of a review is a number between −1 (very negative) and +1 (very positive). For example, the review “Love this! Well made, sturdy, and very comfortable” receives a positive polarity, whereas a review that complains about a product failing after a few days receives a negative one. Sentiment analysis is the most common way of turning review text into a numeric signal for recommender systems [9], [10].

A fake review is a review that is not written by a genuine buyer on the basis of real experience. Recent studies show that such reviews can now be produced by language models and that machine classifiers can separate them from human-written reviews better than human readers can [11], [12]. In baseline investigations, Support Vector Machine (SVM) and VADER were evaluated as candidate algorithms. For deployment, each review is converted to a TF-IDF (Term Frequency–Inverse Document Frequency) vector, which gives a high weight to words that are frequent in one review but rare in the whole collection. A Random Forest classifier, which combines the votes of many decision trees, was found to deliver superior accuracy and recall in separating computer-generated (fake) reviews from original (genuine) reviews.

Price is the third signal. Price-aware recommendation studies show that the price preference of a consumer changes over time and that price tolerance affects what should be recommended [6], [13]. In India, prices also change sharply during festival sales, so the decision of when to buy is as important as where to buy.

The base paper for this work is the spam-aware recommendation framework of Jin, Li and Chen [7]. The authors first detect spam reviews using machine learning and deep learning models built on semantic, sentiment and metadata features, and then allow only the filtered credible reviews to contribute to personalised recommendations. This links review credibility with preference modelling, which most sentiment-based recommenders handled separately [14], [15]. Najib [15] showed that a detailed rating based on factors such as quality, price, speed and usability is more informative than a single overall rating and reported an average accuracy of 93.26%.


## 1.3 PROBLEM STATEMENT

Online shoppers find it difficult to decide which product and which store to choose, because the available information is large, scattered and not always trustworthy. The price of the same product differs between stores, the reviews are spread over many pages, and star ratings alone hide both the opinion contained in the review text and the possibility that the reviews are fake.

The existing systems have the following shortcomings:

- First, most sentiment-based recommenders assume that all reviews are genuine, although fake and AI-generated reviews are now widespread [3], [5].
- Second, price-aware recommenders model price preference from purchase sessions but do not judge the credibility of product reviews [6], [13].
- Third, existing tools seldom combine live multi-store prices, review sentiment and review trust into one understandable score that tells the buyer what to do.
If the problem remains unsolved, buyers may purchase poor products because of manipulated reviews, pay more than necessary and lose trust in e-commerce platforms [16]. Therefore, there is a need for a system that analyses reviews for both sentiment and authenticity, compares prices across stores, and converts the results into a clear and explainable buying recommendation.


## 1.4 AIM OF THE PROJECT

The primary aim of this project is to design and develop an intelligent web-based product recommendation system that collects product prices and customer reviews from multiple e-commerce websites, analyses the sentiment of the reviews using TextBlob, detects fake reviews using TF-IDF features and a Random Forest classifier, and combines a Price Score, a Sentiment Score and a Trust Score into a Value Score that recommends the best store and a BUY NOW, CONSIDER or WAIT decision. The fake review classifier is targeted to reach an accuracy of more than 80% on unseen reviews; the current model achieves 84.27%.


## 1.5 OBJECTIVES OF THE PROJECT

The key objectives of the proposed system are as follows:

- To collect product details, prices and customer reviews from Amazon, Flipkart and Croma product pages using Playwright-based web scrapers and store them in a MySQL database.
- To perform sentiment analysis of every review using TextBlob polarity and classify it as positive, negative or neutral.
- To prepare a labelled dataset of 40,432 reviews and train a TF-IDF and Random Forest classifier that separates genuine (original) reviews from computer-generated (fake) reviews.
- To compute the Sentiment Score, the Trust Score and the Price Score for each product and store.
- To develop a Value Score model with weights of 0.40, 0.30 and 0.30 and a rule-based BUY NOW, CONSIDER or WAIT decision, including analysis of festival discount offers.
- To build a FastAPI backend and a web interface through which users can search products and view price comparison, scores and the recommendation.
- To test the modules and evaluate the fake review model using accuracy, precision, recall and F1-score.

## 1.6 SCOPE AND ORGANIZATION OF THE REPORT

The project covers a browser-based application for Indian online shoppers. Product prices are collected from Amazon.in, Flipkart and Croma pages, English-language text reviews are analysed, and the results are stored in a MySQL database and shown through a web interface. Backpacks (for example, a Safari backpack) are used as the test product category. The fake review model is trained and tested on a public labelled dataset of 40,432 reviews from ten product categories using an 80:20 stratified split. The scrapers are tested on live product pages using Playwright with Chromium on a Windows development machine.

The remainder of this report is organized as follows: Chapter 2 presents a literature survey of 44 relevant research papers covering recommender systems, sentiment analysis, fake review detection and price comparison, and identifies the research gaps. Chapter 3 examines the conventional existing systems, their architecture, algorithms, and key drawbacks. Chapter 4 presents the proposed system architecture, modular descriptions, mathematical formulations, flow chart, and advantages over conventional systems. Chapter 5 concludes Phase 1 and presents the future scope, followed by References.


# CHAPTER 2

**LITERATURE SURVEY**


## 2.1 GENERAL

A total of 44 research papers were surveyed for this project. They were taken from journals and conferences published by Elsevier, Springer, IEEE, MDPI, Taylor & Francis, IGI Global, PLOS, Nature Portfolio and others, and cover the years 2020 to 2026, with 36 of the papers published in 2022 or later. Papers were selected if they dealt with sentiment-based recommendation, sentiment classification of e-commerce reviews, fake review detection, review credibility or price-aware recommendation.

A common trend across the papers is the move from rating-based recommendation to review-based recommendation using deep learning and transformers, and, more recently, towards the problem of AI-generated fake reviews. The chapter is organised in three parts: the review of literature grouped by theme, a summary table comparing the key surveyed papers, and the research gaps derived from the survey.


## 2.2 REVIEW OF LITERATURE


### 2.2.1 Base Paper and Spam-Aware Recommendation

Jin et al. [7] proposed a spam-aware recommendation framework that detects spam reviews with machine learning and deep learning models using semantic, sentiment and metadata features, and lets only the filtered credible reviews contribute to personalised recommendations. It joins review credibility and recommendation, but price information is not part of the described framework.


### 2.2.2 Sentiment-Based and Hybrid Recommender Systems

Karthik and Ganapathy [1] built a fuzzy-rule and ontology-based recommender that uses a new sentiment score for a target user category to predict the current interests of customers, and reported better accuracy and response time than existing systems. Review authenticity and price are not modelled.

Ni et al. [17] combined Spark-ALS rating-based recommendation with sentiment classification on a beer review dataset, comparing ten conventional and deep learning classifiers. Filtering products with many negative reviews improved user acceptance, but the work is limited to one product domain.

Srifi et al. [9] surveyed collaborative filtering recommenders that use review words, topics and sentiments to overcome the weaknesses of rating-based filtering. The survey concentrates on how review text improves filtering; review credibility and price are outside its scope.

Elahi et al. [14] proposed a hybrid recommender that extracts sentiment from reviews and uses it together with ratings. On Amazon Digital Music and Video Games data they showed that sentiment is not always correlated with rating and that the hybrid model outperforms the baselines. Fake reviews and price are not considered.

Yadav [18] extracted customer-cared aspects (price, colour, battery and screen) from Amazon comments using WordNet, classified the aspect comments as positive, negative or neutral, and scored brands for recommendation. The aspect set is small and fixed, and fake reviews are not filtered.

Najib [15] replaced the single overall rating with a detailed rating based on quality, price, speed and usability derived from Amazon review text, and reached up to 97.74% accuracy (average 93.26%). The ratings assume that the reviews are genuine and live multi-store prices are not used.

Feng [19] combined an improved S-PageRank web information extraction method (90% precision across platforms) with a topic-model and BiLSTM attention network that computes topic-level sentiment scores, with the best accuracy at seven LDA topics. Review authenticity is not verified.

Latha and Rao [20] applied TF-IDF vectors and a modified CNN to 60,000 Amazon reviews labelled positive, negative and neutral and obtained a mean accuracy of 97.40%. The system classifies sentiment only and does not use price or review credibility.

Krishna et al. [21] combined feature-level sentiment analysis using MLA-EDTCNet, GAN-based oversampling for class imbalance and an optimisation algorithm for parameter tuning with collaborative filtering on an Amazon dataset, outperforming state-of-the-art models on accuracy, precision, recall, F1-score and AUC. The pipeline is complex and does not assess review authenticity or price.

Kollu and Garapati [22] proposed DeepSentRec, which joins SentimentBERT, a hybrid collaborative and SBERT content similarity, and a reinforcement learning ranker. On four public datasets it obtained 91.12% precision, 85.49% recall, 89.66% NDCG and 24.96% CTR. Fake reviews and price are not part of the ranking signal.

Yi and Liu [23] applied machine learning to classify product and shop information from customer reviews of a benchmark computer-hardware dataset and reported accuracy of nearly 98% with a mean absolute error of about 0.6. The study is restricted to one product type and does not filter fake reviews.

Yang et al. [24] proposed a sentiment-driven fuzzy cloud multi-criteria model that mines product attributes from reviews of several platforms using BiLSTM-CRF, sentiment analysis and K-means, and ranks mobile phones with q-rung orthopair fuzzy clouds. It works across platforms but is mathematically heavy and does not detect fake reviews.

Wang et al. [25] ranked products with an improved PageRank over competitor relations, using attribute performance scores from sentiment and review usefulness. On 41,352 Best Buy reviews it improved the Spearman correlation by up to 18.3% over traditional multi-criteria models. Price is used only to segment the data, and review authenticity is not checked.

Nath Sharma and Sadagopan [26] used dictionary-based sentiment analysis with conditional holoentropy feature selection and a Deep Belief Network tuned by a hybrid swarm optimiser for e-commerce recommendation. The optimisation makes the model complex, and review genuineness and price are not considered.


### 2.2.3 Sentiment Classification and Aspect-Level Analysis

Daza et al. [10] reviewed 20 studies (2018–2024) on sentiment analysis of e-commerce reviews following the PRISMA method and found that SVM and LSTM were among the most accurate techniques, F1-score the key metric and Python the main language. It is a review and does not propose a system.

Gondhi et al. [27] combined LSTM with word2vec on the Amazon Review dataset 2018 and obtained better accuracy, precision, recall and F1-score than baseline models. The work classifies sentiment but does not connect it to recommendation or credibility.

Fang et al. [28] proposed Chinese-BERT-wwm with multi-channel CNN and BiLSTM for sentence-level Chinese product reviews and obtained 94.37% accuracy and 94.34% F1-score on 100,000 reviews. It is limited to Chinese text and binary sentiment.

Bellar et al. [29] benchmarked CNN, RNN and Bi-LSTM models with BERT-based, FastText and Word2Vec embeddings for 5-class and 3-class rating prediction on women’s clothing reviews. The study uses one product domain and does not include recommendation or fake review detection.

Lu et al. [30] proposed semi-supervised sentiment classification in which a tripartite graph and clustering are used for label propagation, handling polysemy and synonymy and working with few labelled samples. Recommendation is not addressed.

Abudureheman [31] designed a comment management system that uses part-of-speech tagging, dependency rules for emotion-word extraction and a BiGRU–TextCNN model, reaching 93.49% accuracy and 96.98% recall for positive comments. The output is only a sentiment label; authenticity and price are not considered.

Davoodi et al. [32] created a manually annotated dataset of 3,500 Trustpilot reviews with fourteen aspects and found RoBERTa to be the best model with more than 90% accuracy for aspect-based sentiment classification of e-commerce platforms. It evaluates platform service rather than product recommendation.

Dey and Jenamani [33] introduced UAN-OACIS, an unsupervised attention-based framework that extracts opinion, aspect, category, irrealis and sentiment quintuples, and showed that handling irrealis improves sentiment scores over lexicon methods. It targets aspect extraction and not recommendation.

Valencia-Arias et al. [2] performed a bibliometric analysis of AI and recommender systems in e-commerce (91 documents analysed), observed a shift towards sentiment analysis and convolutional networks in 2021–2022, and suggested knowledge graphs and content-based image retrieval as future areas.


### 2.2.4 Fake Review Detection

Yu et al. [4] surveyed graph-learning methods for fake review, fake reviewer and fake review analysis, covering supervised and unsupervised approaches and open problems such as imperfect data, explainability and model efficiency.

Mewada and Dewang [3] reviewed false review detection methods for hotel and e-commerce domains, compared review and spammer features, and pointed out problems in obtaining large labelled datasets and in feature and method design.

Luo et al. [5] proposed a supervised approach for detecting AI-generated fake reviews that uses an outlier-detection method based on cumulative probability density and an AdaBoost classifier, and showed higher detection accuracy than several baselines. The work stops at detection and is not linked to recommendation.

Naveen and Handa [12] systematically reviewed fake review detection research from 2020 to 2025 with a taxonomy of machine learning, deep learning, transformer, graph, swarm and hybrid methods, and noted that conventional detectors struggle with LLM-generated reviews. Explainability, dataset validity and real-time deployment remain open challenges.

Mohawesh et al. [34] combined RoBERTa with an LSTM layer and used SHAP and attention for explanation, achieving 96.03% accuracy on the OpSpam dataset and 93.15% on the Deception dataset. The datasets are semi-real benchmarks and the work is limited to detection.

Salminen et al. [11] generated fake reviews with GPT-2 and ULMFiT from an Amazon dataset and showed that a machine classifier detects them almost perfectly while human raters perform much worse. This supports the use of a classifier for computer-generated reviews.

Mohawesh et al. [35] proposed an explainable ensemble of Bi-LSTM, CNN and DNN models using review content, reviewer data and product description, improving AUC by 1% to 7% over state-of-the-art methods on two real datasets, with SHAP-based explanations.

Qandos et al. [36] introduced the Arabic Fake Reviews Detection dataset for hotels, restaurants and products and a multiscale cascaded approach that transfers knowledge between domains and improved accuracy by 2.09% to 7.8%. It is limited to the Arabic language.

Jayasinghe and Dassanayaka [37] separated genuine and fraudulent Amazon reviews of verified and non-verified purchases using the bootstrap distribution of cosine similarity, a CNN with word embeddings and emotion mining, and a new loss function, reaching accuracy above 96%.

Bikku et al. [38] applied a quantum neural network to an Amazon fraudulent review dataset and reported 86% accuracy, while noting that quantum machine learning is still at an early stage of development.

Zhong et al. [39] detected deceptive reviews on Taobao data with a semi-supervised method that builds a time series of reviews, finds burst intervals and applies co-training on linguistic, metadata and purchase-behaviour views, balancing accuracy and efficiency while reducing the need for labelled data.

Soldner et al. [40] showed experimentally that product ownership and data origin act as confounds in fake review detection: accuracy of 60.26–69.87% for veracity alone rose to 87.78–88.12% when both confounds were present, suggesting that earlier studies may have overestimated detection accuracy.

Das et al. [41] proposed an explainable Fake Review Index that combines structured review metadata with a semantic topic index and applies LIME to derive a confidence score, aimed at small and medium retailers on Amazon.

Schneider and Teubner [16] estimated the proportion of potentially fake five-star ratings in Airbnb’s closed reputation system from differences between first and second rating distributions using KL-divergence, and showed that early reputation is important for new sellers.


### 2.2.5 Review Credibility

Jha and Shah [42] conducted a controlled experiment showing that disconfirmation between expected and actual experience affects how a review is written and its perceived credibility, with a U-shaped relationship.

Mumuni et al. [43] showed that review relevance is almost as strong a driver of online product review impact as review credibility, and that credibility is positively related to reviewer trustworthiness but negatively related to expertise.

Pooja and Upadhyaya [44] systematically reviewed 69 empirical papers and grouped the antecedents of review credibility into source, review, consumer, interpersonal and product-type characteristics.


### 2.2.6 Price-Aware Recommendation

Guo et al. [6] proposed a deep learning recommender that models the dynamic price and product preferences of consumers using a review-and-rating-based sequence generator and a multi-level attention transformer, and outperformed state-of-the-art models on real datasets.

Feng et al. [13] proposed PASBR, a price-aware session-based recommender using graph neural networks that models price tolerance, category-level intent and dynamic interest, and outperformed baselines on two real datasets. It works on session data and not on review quality.

De Biasio et al. [8] surveyed 135 papers on economic recommender systems that include price awareness and profitability and classified the approaches, evaluation methods and limitations. None of the surveyed papers combines review sentiment, a classifier-based review trust estimate, live multi-store prices and a buy-or-wait decision in one deployable system.


## 2.3 COMPARATIVE SUMMARY TABLE OF LITERATURE SURVEY

Table 2.1 provides a structured comparative summary of selected key papers from the literature survey, highlighting the methods used, their main findings and limitations.

**Table 2.1. Comparative Summary Table of Selected Key Literature**


| Author(s) & Year | Ref | Methodology | Key Findings | Limitations |
| --- | --- | --- | --- | --- |
| Karthik & Ganapathy [1] | 2021 | Fuzzy Rules + Ontology + Sentiment | Predicts customer interest with fast response time | Single platform; assumes all reviews genuine; ignores price |
| Valencia-Arias et al. [2] | 2024 | Bibliometric Analysis (91 papers) | Identified shift towards deep learning and review sentiment | Bibliometric survey only; no system developed |
| Mewada & Dewang [3] | 2022 | Literature Survey on Spam Detection | Compared review-centric and reviewer-centric spam features | Points out shortage of real ground-truth datasets |
| Yu et al. [4] | 2022 | Graph Neural Networks | Surveys graph learning for fake review and spammer rings | High computational cost; needs platform-internal data |
| Luo et al. [5] | 2026 | Outlier Detection + AdaBoost | Effectively detects AI-generated fake reviews | Classification only; not connected to recommendation |
| Guo et al. [6] | 2023 | Sequence Generator + Attention Transformer | Models dynamic consumer price preference over time | Focuses on sessions; does not filter fake reviews |
| Jin et al. [7] (Base Paper) | 2026 | Spam Detection + Filtered Recommendation | Proved that removing spam reviews improves recommendation | Single store; no live multi-store prices; no buy/wait advice |
| De Biasio et al. [8] | 2024 | Economic Recommenders Survey (135 papers) | Classifies price-aware and profit-aware recommendation systems | Notes lack of consumer-advocate decision tools |
| Srifi et al. [9] | 2020 | Collaborative Filtering Survey | Surveys text and sentiment in collaborative filtering | Review credibility and price are outside the scope |
| Daza et al. [10] | 2024 | PRISMA Systematic Review (20 papers) | Identified SVM and LSTM as most accurate sentiment methods | Survey only; does not implement a working tool |
| Salminen et al. [11] | 2021 | GPT-2 / ULMFiT + Supervised ML | Proved machines detect AI reviews better than human raters | Benchmarking experiment; not deployed as a web tool |
| Naveen & Handa [12] | 2026 | Systematic Review (2020-2025) | Taxonomy of ML, deep learning and transformer detectors | Notes explainability and real-time deployment are open gaps |
| Feng et al. [13] | 2023 | Graph Neural Network (PASBR) | Models price tolerance and category intent from sessions | Works on click streams; ignores review authenticity |
| Elahi et al. [14] | 2023 | Hybrid Rating + Sentiment Model | Showed sentiment often disagrees with numerical rating | Assumes reviews are genuine; no price comparison |
| Najib [15] | 2026 | Multi-Attribute Rating Strategy | Replaces single rating with quality, price, speed scores (93.26%) | Assumes reviews are genuine; no live multi-store prices |
| Soldner et al. [40] | 2022 | Confound Analysis in Fake Reviews | Showed product ownership and data origin inflate accuracy | Emphasizes need for clean balanced text datasets |


## 2.4 RESEARCH GAP

The survey leads to the following four key research gaps:

First, review-based recommenders and fake review detectors are developed separately. Recommenders such as [1], [14], [15], [22] use review sentiment as if every review were genuine, while detection studies such as [5], [34], [37] stop at classifying reviews. Only the framework of [7] connects the two. Our system fills this gap by turning the output of a Random Forest fake review classifier into a Trust Score that is used directly in the recommendation.

Second, price-aware recommenders model price preference from purchase sessions or sequences [6], [8], [13] and do not judge the credibility of reviews, while the multi-platform model of [24] uses sentiment but neither price nor fake review detection. Our system fills this gap with a Price Score computed from live prices of several stores and combined with the sentiment and trust of the reviews.

Third, many strong models are computationally complex, such as transformer, quantum and optimiser-tuned networks [21], [34], [38], and the studies end with a classification result instead of advice to the buyer. Detection accuracy may also be overestimated because of data confounds [40]. Our system fills this gap with a light, explainable scoring pipeline and rule-based decision (BUY NOW, CONSIDER or WAIT) that uses festival discount information, delivered through a web interface.

Fourth, existing proposals are mostly evaluated on static offline datasets without testing whether real-time data collection from active e-commerce product pages is practical. Our project bridges this gap by implementing automated Playwright scrapers that extract live prices, discounts and reviews directly from Amazon, Flipkart and Croma.


# CHAPTER 3

**CONVENTIONAL SYSTEM**


## 3.1 GENERAL

This chapter describes the conventional approaches on which modern e-commerce recommendations and shopping portals operate, analyzes the base paper on which this project builds, and discusses the detailed drawbacks of conventional systems. The proposed system, its architecture, modules and workflow are covered in Chapter 4.

Online consumer retail has traditionally grown around individual marketplace platforms such as Amazon, Flipkart, Croma and eBay. In these platforms, products are listed by sellers, ratings are collected from buyers, and recommendation algorithms suggest products to users while they browse. When an online shopper intends to purchase a product, the platform typically presents a list of related items ranked by popularity, sponsored ad priority or collaborative filtering. The shopper clicks on a product, inspects the average star rating, reads a few recent reviews, checks the displayed price, and decides whether to proceed to checkout.

While these conventional systems are widely used, they were designed around a single store and assume that reviews and ratings are honest. In modern online shopping, this assumption causes significant issues for consumers because prices vary between stores and fake reviews are common.


## 3.2 ARCHITECTURE AND WORKING OF CONVENTIONAL SYSTEMS

The architecture of a conventional e-commerce recommendation system operates strictly within a single platform. The typical workflow is as follows:

- User Search Input: The shopper enters a keyword or product category in the store's search bar.
- Catalog Retrieval: The platform's internal database retrieves products matching the keyword.
- Ranking and Collaborative Filtering: Candidate products are ranked using historical user interaction logs, ratings and seller advertising bids.
- Average Rating Computation: The store calculates an arithmetic mean of all 1-star to 5-star ratings submitted for the product and displays it as the primary quality indicator.
- Single-Store Transaction: The buyer views the price listed on that store and completes the purchase.
In this traditional flow, there is no communication between different e-commerce platforms. If the same backpack is sold on Flipkart for INR 1,199 and on Amazon for INR 1,299, the Amazon platform will never inform the shopper about the lower price on Flipkart. Furthermore, because all submitted ratings are averaged together, even an inferior product can achieve a high 4.5-star average if the seller purchases fake 5-star reviews.


## 3.3 METHODOLOGIES AND ALGORITHMS USED IN EXISTING SYSTEMS

Conventional recommendation systems rely heavily on Collaborative Filtering (CF). Collaborative filtering predicts a user's interest in an item based on the preferences of other similar users. The two standard types are User-Based Collaborative Filtering and Item-Based Collaborative Filtering.

In User-Based Collaborative Filtering, the similarity between user u and user v is commonly computed using the Pearson Correlation Coefficient:

**sim(u, v) = Σ (r_{u,i} − r̄_u)(r_{v,i} − r̄_v) ÷ √[ Σ (r_{u,i} − r̄_u)² × Σ (r_{v,i} − r̄_v)² ]**

In Item-Based Collaborative Filtering, the similarity between item i and item j is calculated using Cosine Similarity over user rating vectors:

**sim(i, j) = (i · j) ÷ (||i|| × ||j||) = Σ (r_{u,i} × r_{u,j}) ÷ √[ Σ (r_{u,i})² × Σ (r_{u,j})² ]**

For rating aggregation, traditional stores compute the simple average star rating:

**Average Rating = (1 / N) × Σ rᵢ**

Table 3.1 summarizes the algorithms used in conventional systems and their practical limitations.

**Table 3.1. Algorithms Used in Conventional Systems and Their Practical Limitations**


| Method | How It Operates | Limitation in Online Shopping |
| --- | --- | --- |
| User-Based CF | Finds users with similar rating history | Suffers from sparse data; easily fooled by fake reviewer accounts |
| Item-Based CF | Finds items frequently bought together | Cold start problem for new items; completely ignores store prices |
| Average Rating | Arithmetic mean of 1 to 5 star ratings | Treats fake reviews the same as real reviews; hides review sentiment |
| Manual Price Comparison | Shopper manually opens multiple browser tabs | Slow, tedious, and prone to human error |


## 3.4 ANALYSIS OF THE BASE PAPER

The base paper for this project is the spam-aware recommendation framework of Jin, Li and Chen [7]. Most e-commerce platforms, in contrast, still present the overall numerical rating as the main indicator of product quality [15]. The framework of [7] works as follows:

- Input: customer reviews of products together with review metadata and the user preferences needed for personalised recommendation.
- Spam detection: machine learning and deep learning models classify each review as spam or credible using semantic, sentiment and metadata features.
- Filtering: reviews that are classified as spam are removed so that only trustworthy reviews remain.
- Recommendation: the filtered credible reviews are used in preference modelling to generate personalised product recommendations.
- Output: a list of recommended products that is more reliable and better aligned with the user’s preferences.
The authors report that using only credible reviews gives more reliable and preference-aligned suggestions and supports more confident purchase decisions [7]. The related detailed-rating approach of [15] applies sentiment analysis to Amazon reviews for factors such as quality, price, speed and usability and reports an accuracy of up to 97.74%.

However, the base paper has three notable limitations: (i) it does not incorporate product price or cross-store price comparison, (ii) it simply removes spam without computing an explicit Trust Score, and (iii) it outputs a product list rather than an actionable BUY NOW or WAIT decision.


## 3.5 DRAWBACKS OF EXISTING SYSTEMS

Conventional e-commerce recommendation systems suffer from the following specific drawbacks:

- Single-Store Price Blindness: Existing methods concentrate on reviews within one platform and do not compare the live price of the same product across different stores, so the buyer still has to search for the best price manually.
- Assumption of Genuine Reviews: Sentiment-based recommenders assume that reviews are genuine [14], [15], which allows fake and computer-generated reviews to distort the result.
- No Clear Purchase Timing Guidance: The output of conventional tools is a ranked list or a rating and not a clear instruction on whether to buy now or wait, even when festival discounts are available.
- High Computational Overhead: Several high-accuracy models in the literature rely on complex deep learning, transformer or optimisation components that need GPU resources and are hard to explain to the end user.
- Offline Research Prototypes: Many proposals in the literature are research prototypes evaluated offline on static historical datasets and are not delivered as a working web application with automatic data collection.

# CHAPTER 4

**PROPOSED SYSTEM**


## 4.1 GENERAL AND PROPOSED SYSTEM ARCHITECTURE

This chapter presents the proposed system and its advantages, the system architecture, the description of the modules, the mathematical scoring formulation, and the flow chart of the system. The proposed system keeps the idea of the base paper that only trustworthy review information should drive a recommendation, and adds live price comparison across stores and a decision stage.

The architecture of the proposed system is shown in Figure 4.1. The user interacts with the browser-based frontend written in HTML, CSS and JavaScript, which sends HTTP requests to the FastAPI backend. The backend reads from and writes to the MySQL database through the SQLAlchemy ORM. The data acquisition module (Module 1) stores prices and reviews, the sentiment analysis (Module 2) and fake review detection (Module 3) modules analyse the stored reviews, and the score computation (Module 4), recommendation engine (Module 5) and festival offer analysis (Module 6) use these results to produce the best store, the Value Score and the buy decision, which are returned to the user.

**Fig. 4.1. System Architecture of the Intelligent Product Recommendation System**


## 4.2 MODULE DESCRIPTION

The proposed system is divided into six functional modules:

- Module 1 - Data Acquisition (Web Scraping): Playwright launches Chromium, opens the product pages of Amazon, Flipkart and Croma, and extracts the product name, current price, original price, discount, and reviews. Flipkart reviews are read from verified buyer blocks, and Croma data is read from JSON-LD metadata. Data is stored in MySQL.
- Module 2 - Sentiment Analysis: The polarity p of each review is calculated with TextBlob. The review is labelled Positive (p > 0), Negative (p < 0) or Neutral (p = 0), and the sentiment strength is |p|. In baseline tests, VADER was benchmarked, while TextBlob provided consistent polarity mapping.
- Module 3 - Fake Review Detection: Each review is converted to a TF-IDF vector (5,000 features, English stop words removed). A Random Forest classifier with 200 trees, trained on 40,432 labelled reviews, gives the probability f that the review is fake. The model achieves 84.27% accuracy on 8,087 unseen test reviews, outperforming baseline SVM.
- Module 4 - Score Computation: Computes the Sentiment Score, Trust Score and Price Score for each store using Equations 4.1 to 4.3.
- Module 5 - Value Score and Recommendation Engine: Combines the component scores using Equation 4.4 into a Value Score (0–100) and selects the best store.
- Module 6 - Festival Offer Analysis: Analyzes promotional discount percentages to provide purchase advice.

## 4.3 MATHEMATICAL FORMULATION AND SCORING LOGIC

The scoring engine converts the extracted price, sentiment, and fake probabilities into three normalized scores between 0 and 100, and computes a composite Value Score using the following equations:

**Sentiment Score = (1/n) × Σ |pᵢ| × 100				(4.1)**

**Trust Score = (1/n) × Σ (1 − fᵢ) × 100				(4.2)**

**Price Score = (lowest price ÷ store price) × 100			(4.3)**

**Value Score = 0.40 × Price + 0.30 × Sentiment + 0.30 × Trust	(4.4)**

Here n is the number of reviews of the product, pᵢ is the polarity of review i and fᵢ is its fake probability. In the web interface, the decision thresholds are: Value Score ≥ 70 gives BUY NOW, 50 to 69.99 gives CONSIDER, and below 50 gives WAIT. For festival offers, a discount of 60% or more gives BUY NOW and a lower discount gives WAIT.

Table 4.1 shows an illustrative Value Score calculation with assumed prices of ₹1,299 (Amazon) and ₹1,199 (Flipkart) and sample Sentiment Score 58.19 and Trust Score 37.43.

**Table 4.1. Illustrative Value Score Calculation for Benchmark Product**


| Store | Price (₹) | Price Score | Sentiment | Trust | Value Score | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| Flipkart | 1,199 | 100.00 | 58.19 | 37.43 | 68.69 | CONSIDER |
| Amazon | 1,299 | 92.30 | 58.19 | 37.43 | 65.61 | CONSIDER |


## 4.4 SYSTEM FLOW CHART AND DECISION HEURISTICS

Figure 4.2 shows the operational flow of the system. The process starts when the user enters or selects a product. Prices are scraped from the stores and the reviews are collected and stored in the database. Each review is analysed for sentiment and for the probability of being fake, and the Sentiment Score and the Trust Score are calculated. The Price Score is calculated from the store prices and the three scores are combined into the Value Score. If the Value Score is 70 or more (Yes), the decision is BUY NOW; otherwise, if it is 50 or more (Yes), the decision is CONSIDER, and if not (No), the decision is WAIT. The process ends after the decision is displayed.

**Fig. 4.2. Flow Chart of the Intelligent Product Recommendation System**


## 4.5 ADVANTAGES AND COMPARISON WITH EXISTING SYSTEM

The proposed system offers several practical advantages over conventional recommendation methods:

- Live prices of several stores are compared automatically, which removes the manual search for the best price.
- The Trust Score lowers the influence of suspicious reviews, which addresses the assumption that all reviews are genuine.
- One Value Score with visible components makes the recommendation easy to understand and explain.
- The BUY NOW, CONSIDER or WAIT output and festival offer analysis give the buyer a clear action.
- TF-IDF with Random Forest and TextBlob are light, run on a normal computer without GPU and are easy to retrain.
- A FastAPI backend and web interface make the system usable as a working application.
**Table 4.2. Feature Comparison between Conventional System and Proposed System**


| Feature | Conventional System | Proposed System |
| --- | --- | --- |
| Store Coverage | Single store only | Multi-store (Amazon, Flipkart, Croma) |
| Price Comparison | None (manual) | Automated real-time Price Score |
| Review Analysis | Raw star rating average | TextBlob polarity sentiment analysis |
| Fake Review Filtering | None (assumes all genuine) | TF-IDF + Random Forest (84.27% accuracy) |
| Decision Output | Ranked list or overall rating | Actionable BUY NOW / CONSIDER / WAIT |
| Hardware Requirement | High (for deep learning) | Normal computer (no GPU needed) |


# CHAPTER 5

**CONCLUSION AND FUTURE SCOPE**

**5.1 CONCLUSION**

Online shoppers frequently face difficulties in identifying the best deal across stores and verifying whether product reviews are authentic. In this Phase-1 project, an Intelligent Product Recommendation System was developed to resolve these issues. The system collects live prices and reviews from Amazon, Flipkart, and Croma using Playwright scrapers, computes review sentiment polarity with TextBlob, and detects computer-generated fake reviews using TF-IDF features and a Random Forest classifier.

Trained on a benchmark dataset of 40,432 labelled reviews, the model achieved an accuracy of 84.27% and a recall of 87.09% on unseen test data. The system combines Price, Sentiment, and Trust into a single Value Score (0.40 * Price + 0.30 * Sentiment + 0.30 * Trust) to deliver clear BUY NOW, CONSIDER, or WAIT purchasing advice. The pipeline is lightweight, runs on commodity CPU hardware without a GPU, and is delivered through a FastAPI backend and web interface.

**5.2 FUTURE SCOPE**

The planned enhancements for Phase 2 of this project include:

- Aspect-Based Sentiment Analysis (ABSA): Implementing transformer models to extract sentiment on specific product features such as durability, quality, and battery life.
- 7-Day Price Forecasting: Training time-series models on historical price logs to predict upcoming price drops and festival discount trends.
- Automated Product URL Ingestion: Enabling users to paste direct product URLs from any store for instantaneous, cross-platform comparative intelligence.
- Cloud Deployment and Live User Testing: Hosting the full stack on cloud infrastructure and evaluating consumer satisfaction through live trials.

# REFERENCES

[1] R.V. Karthik, Sannasi Ganapathy. A fuzzy recommendation system for predicting the customers interests using sentiment analysis and ontology in e-commerce. Applied Soft Computing, 2021. https://doi.org/10.1016/j.asoc.2021.107396

[2] Alejandro Valencia-Arias, Hernan Uribe-Bedoya, Juan David Gonzalez-Ruiz, Gustavo Sanchez Santos, Edgard Chaponan Ramirez, Ezequiel Martinez Rojas. Artificial intelligence and recommender systems in e-commerce. Trends and research agenda. Intelligent Systems with Applications, 2024. https://doi.org/10.1016/j.iswa.2024.200435

[3] Arvind Mewada, Rupesh Kumar Dewang. Research on false review detection methods: A state-of-the-art review. Journal of King Saud University - Computer and Information Sciences, 2022. https://doi.org/10.1016/j.jksuci.2021.07.021

[4] Shuo Yu, Jing Ren, Shihao Li, Mehdi Naseriparsa, Feng Xia. Graph Learning for Fake Review Detection. Frontiers in Artificial Intelligence, 2022. https://doi.org/10.3389/frai.2022.922589

[5] Jiwei Luo, Guofang Nan, Dahui Li. AI-generated fake review detection. Decision Support Systems, 2026. https://doi.org/10.1016/j.dss.2026.114628

[6] Wenhao Guo, Jin Tian, Minqiang Li. Price-aware enhanced dynamic recommendation based on deep learning. Journal of Retailing and Consumer Services, 2023. https://doi.org/10.1016/j.jretconser.2023.103500

[7] Bih-Huang Jin, Yung-Ming Li, Rou-Jyun Chen. Enhancing e-commerce recommendations: A mechanism to detect and mitigate spam reviews. Electronic Markets, 2026. https://doi.org/10.1007/s12525-026-00905-z

[8] Alvise De Biasio, Nicolo Navarin, Dietmar Jannach. Economic recommender systems - a systematic review. Electronic Commerce Research and Applications, 2024. https://doi.org/10.1016/j.elerap.2023.101352

[9] Mehdi Srifi, Ahmed Oussous, Ayoub Ait Lahcen, Salma Mouline. Recommender Systems Based on Collaborative Filtering Using Review Texts - A Survey. Information, 2020. https://doi.org/10.3390/info11060317

[10] Alfredo Daza, Nestor Daniel Gonzalez Rueda, Mirelly Sonia Aguilar Sanchez, Wilmer Filomeno Robles Espiritu, Maria Elena Chauca Quinones. Sentiment Analysis on E-Commerce Product Reviews Using Machine Learning and Deep Learning Algorithms: A Bibliometric Analysis, Systematic Literature Review, Challenges and Future Works. International Journal of Information Management Data Insights, 2024. https://doi.org/10.1016/j.jjimei.2024.100267

[11] Joni Salminen, Chandrashekhar Kandpal, Ahmed Mohamed Kamel, Soon-gyo Jung, Bernard J. Jansen. Creating and detecting fake reviews of online products. Journal of Retailing and Consumer Services, 2021. https://doi.org/10.1016/j.jretconser.2021.102771

[12] Naveen, Disha Handa. AI-Generated Fake Review Detection in E-Commerce: A Unified Taxonomy and Multi-Stakeholder Roadmap. Computers in Human Behavior: Artificial Humans, 2026. https://doi.org/10.1016/j.chbah.2026.100359

[13] J. Feng, Y. Wang, S. Chen. Modeling Price-Aware Session-Based Recommendation Based on Graph Neural Network. Computers, Materials & Continua, 2023. https://doi.org/10.32604/cmc.2023.038741

[14] Mehdi Elahi, Danial Khosh Kholgh, Mohammad Sina Kiarostami, Mourad Oussalah, Sorush Saghari. Hybrid recommendation by incorporating the sentiment of product reviews. Information Sciences, 2023. https://doi.org/10.1016/j.ins.2023.01.051

[15] F. M. Najib. A new detailed rating strategy for enhancing online products recommendation using machine learning and sentiment analysis. Social Network Analysis and Mining, 2026. https://doi.org/10.1007/s13278-026-01583-7

[16] F. Schneider, T. Teubner. Fake It Till You Make It - A Statistical Assessment of the Proportion of Fake Reviews in Closed Reputation Systems. International Journal of Electronic Commerce, 2024. https://doi.org/10.1080/10864415.2024.2401949

[17] Pin Ni, Yuming Li, Victor Chang. Recommendation and Sentiment Analysis Based on Consumer Review and Rating. International Journal of Business Intelligence Research, 2020. https://doi.org/10.4018/IJBIR.2020070102

[18] N. B. Yadav. Harnessing Customer Feedback for Product Recommendations: An Aspect-Level Sentiment Analysis Framework. 2023. https://doi.org/10.1007/s44230-023-00018-2

[19] Jinfeng Feng. E-commerce recommender system design based on web information extraction and sentiment analysis. PLOS ONE, 2025. https://doi.org/10.1371/journal.pone.0327213

[20] Y. M. Latha, B. S. Rao. Amazon product recommendation system based on a modified convolutional neural network. ETRI Journal, 2024. https://doi.org/10.4218/etrij.2023-0162

[21] E. S. Phalguna Krishna, T. Bhargava Ramu, R. Krishna Chaitanya, M. Sitha Ram, Narasimhula Balayesu, Hari Prasad Gandikota, B. N. Jagadesh. Enhancing E-commerce recommendations with sentiment analysis using MLA-EDTCNet and collaborative filtering. Scientific Reports, 2025. https://doi.org/10.1038/s41598-025-91275-7

[22] Siva Rama Prasad Kollu, Yugandhar Garapati. DeepSentRec: a deep learning-based sentiment-aware product recommendation system. Scientific Reports, 2026. https://doi.org/10.1038/s41598-026-45953-9

[23] Shanshan Yi, Xiaofang Liu. Machine learning based customer sentiment analysis for recommending shoppers, shops based on customers' review. Complex & Intelligent Systems, 2020. https://doi.org/10.1007/s40747-020-00155-2

[24] Z. Yang, Q. Li, V. Charles, B. Xu, S. Gupta. Online Product Decision Support Using Sentiment Analysis and Fuzzy Cloud-Based Multi-Criteria Model Through Multiple E-Commerce Platforms. IEEE Transactions on Fuzzy Systems, 2023. https://doi.org/10.1109/TFUZZ.2023.3269741

[25] Xiaoli Wang, Chenxi Zhang, Zeshui Xu. A product recommendation model based on online reviews: Improving PageRank algorithm considering attribute weights. Journal of Retailing and Consumer Services, 2024. https://doi.org/10.1016/j.jretconser.2024.104052

[26] Shambhu Nath Sharma, Prasanna Sadagopan. Influence of conditional holoentropy-based feature selection on automatic recommendation system in E-commerce sector. Journal of King Saud University - Computer and Information Sciences, 2022. https://doi.org/10.1016/j.jksuci.2020.12.022

[27] Naveen Kumar Gondhi, Chaahat, Eishita Sharma, Amal H. Alharbi, Rohit Verma, Mohd Asif Shah. Efficient Long Short-Term Memory-Based Sentiment Analysis of E-Commerce Reviews. 2022. https://doi.org/10.1155/2022/3464524

[28] Hong Fang, Guangjie Jiang, Desheng Li. Sentiment analysis based on Chinese BERT and fused deep neural networks for sentence-level Chinese e-commerce product reviews. Systems Science & Control Engineering, 2022. https://doi.org/10.1080/21642583.2022.2123060

[29] Oumaima Bellar, Amine Baina, Mostafa Ballafkih. Sentiment Analysis: Predicting Product Reviews for E-Commerce Recommendations Using Deep Learning and Transformers. Mathematics, 2024. https://doi.org/10.3390/math12152403

[30] Xin Lu, Donghong Gu, Haolan Zhang, Zhengxin Song, Qianhua Cai, Hongya Zhao, Haiming Wu. Semi-Supervised Sentiment Classification on E-Commerce Reviews Using Tripartite Graph and Clustering. International Journal of Data Warehousing and Mining, 2022. https://doi.org/10.4018/IJDWM.307904

[31] Abuduaini Abudureheman. Design of a User Comment Management System Based on Text Mining. Journal of Organizational and End User Computing, 2023. https://doi.org/10.4018/JOEUC.326611

[32] Laleh Davoodi, Jozsef Mezei, Markku Heikkila. Aspect-Based Sentiment Classification of User Reviews to Understand Customer Satisfaction of E-Commerce Platforms. Electronic Commerce Research, 2025. https://doi.org/10.1007/s10660-025-09948-4

[33] Atanu Dey, Mamata Jenamani. Aspect based sentiment analysis of consumer reviews using unsupervised attention neural framework. Applied Soft Computing, 2024. https://doi.org/10.1016/j.asoc.2024.112259

[34] Rami Mohawesh, Haythem Bany Salameh, Yaser Jararweh, Mohannad Alkhalaileh, Sumbal Maqsood. Fake review detection using transformer-based enhanced LSTM and RoBERTa. International Journal of Cognitive Computing in Engineering, 2024. https://doi.org/10.1016/j.ijcce.2024.06.001

[35] Rami Mohawesh, Shuxiang Xu, Matthew Springer, Yaser Jararweh, Muna Al-Hawawreh, Sumbal Maqsood. An Explainable Ensemble of Multi-View Deep Learning Model for Fake Review Detection. Journal of King Saud University - Computer and Information Sciences, 2023. https://doi.org/10.1016/j.jksuci.2023.101644

[36] Nour Qandos, Ghadir Hamad, Maitha Alharbi, Shatha Alturki, Waad Alharbi, Arwa A. Albelaihi. Multiscale Cascaded Domain-Based Approach for Arabic Fake Reviews Detection in E-Commerce Platforms. Journal of King Saud University - Computer and Information Sciences, 2024. https://doi.org/10.1016/j.jksuci.2024.101926

[37] J. M. Thilini Jayasinghe, Sachith Dassanayaka. Detecting Deception: Employing Deep Neural Networks for Fraudulent Review Detection on Amazon. Neural Computing and Applications, 2025. https://doi.org/10.1007/s00521-025-11485-y

[38] Thulasi Bikku, Srinivasarao Thota, P. Shanmugasundaram. A Novel Quantum Neural Network Approach to Combating Fake Reviews. 2024. https://doi.org/10.1007/s44227-024-00028-x

[39] Minjuan Zhong, Zhenjin Li, Shengzong Liu, Bo Yang, Rui Tan, Xilong Qu. Fast Detection of Deceptive Reviews by Combining the Time Series and Machine Learning. 2021. https://doi.org/10.1155/2021/9923374

[40] Felix Soldner, Bennett Kleinberg, Shane D. Johnson. Confounds and overestimations in fake review detection: Experimentally controlling for product-ownership and data-origin. PLOS ONE, 2022. https://doi.org/10.1071/journal.pone.0277869

[41] Ronnie Das, Wasim Ahmed, Kshitij Sharma, Mariann Hardey, Yogesh K. Dwivedi, Ziqi Zhang, Chrysostomos Apostolidis, Raffaele Filieri. Towards the development of an explainable e-commerce fake review index: An attribute analytics approach. European Journal of Operational Research, 2024. https://doi.org/10.1016/j.ejor.2024.03.008

[42] Ashish Kumar Jha, Snehal Shah. Disconfirmation effect on online review credibility: An experimental analysis. Decision Support Systems, 2021. https://doi.org/10.1016/j.dss.2021.113519

[43] A. G. Mumuni, K. O'Reilly, A. MacMillan, S. Cowley, B. Kelley. Online Product Review Impact: The Relative Effects of Review Credibility and Review Relevance. Journal of Internet Commerce, 2020. https://doi.org/10.1080/15332861.2019.1700740

[44] K. Pooja, P. Upadhyaya. What makes an online review credible? A systematic review of the literature and future research directions. Management Review Quarterly, 2022. https://doi.org/10.1007/s11301-022-00312-6
