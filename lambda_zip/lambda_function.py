import json
import re
from textblob import classifiers
from textblob import TextBlob
	
alphabets="([A-Za-z])"
prefixes="(Mr|St|Mrs|Ms|Dr)[.]"
suffixes="(Inc|Ltd|Jr|Sr|Co)"
starters="(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms="([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites="[.](com|net|org|io|gov)"

def split_into_sentences(text):
   text = " " + text + "  "
   text = text.replace("\n"," ")
   text = re.sub(prefixes,"\\1<prd>",text)
   text = re.sub(websites,"<prd>\\1",text)
   if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
   text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
   text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
   text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
   text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
   text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
   text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
   text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
   if "”" in text: text = text.replace(".”","”.")
   if "\"" in text: text = text.replace(".\"","\".")
   if "!" in text: text = text.replace("!\"","\"!")
   if "?" in text: text = text.replace("?\"","\"?")
   text = text.replace(".",".<stop>")
   text = text.replace("?","?<stop>")
   text = text.replace("!","!<stop>")
   text = text.replace("<prd>",".")
   sentences = text.split("<stop>")
   sentences = sentences[:-1]
   sentences = [s.strip() for s in sentences]
   return sentences
		
def lambda_handler(event, context):


   training2 = [
	("Bachelor Degree or Diploma","skill"),
	("At least 3 years of working experience","skill"),
	("Proficiency in using React, HTML5, CSS3 and JavaScript GIT,Babel.js","skill"),
	("Strong experience with Redux, React-Router, Component-container design pattern.","skill"),
	("Knowledge of Redux","skill"),
	("Knowledge on Webpack and Chrome Dev","skill"),
	("Implement the front-end technical design and development.","task"),
	("Write robust front-end code using React frameworks and libraries.","task"),
	("Develop rich, interactive data visualizations, and other dynamic features.","task"),
	("Rapidly design, prototype and iterate on creative concepts to meet the user requirements.","task"),
	#("As our Front End Web Developer, you will be responsible for creating a fully functional user interface that enhances the experience of our customers.","role_desc"),
	("As our Front End Web Developer, you will be responsible.","role_desc"),
	("You will be responsible for the experience of our customers.","role_desc"),
	("As our Front End Developer, you will be responsible for creating a fully functional user interface","role_desc"),
	("As our Front End Web Developer, you will be responsible for enhances the experience of our customers.","role_desc"),
	#("In this role, your input will be directly reflexted in the products we develope and define pathways
	#for future features to pursue.","role_desc"),
	("In this role, you will develop and define pathways","role_desc"),
	("In this role, your input will be directly reflected in the products we develop","role_desc"),
	("In this role, you will develop the products for enhancing the experience of our customers","role_desc"),
	("You will be able to define pathways for future features.","role_desc"),
	("you will be part of our Technology team, working to develop and maintain high quality web application.","role_desc"),
	("You will be taking lead and ownership of the development of our official website and web applications.","role_desc"),
	("As our Front End Web Developer, you'll collaborate with internal teams to develop functional web applications, while working in a fast-paced environment.","role_desc"),
	("Ultimately, you will be building the next generation of our web applications.","role_desc"),
	("Use product requirements, mock-ups and wireframes and develop them into fully functioning web applications by writing clean code.","task"),
	("Support the entire web application lifecycle (code, test, debug, release and support).","task"),
	("Collaborate with back-end developers and designers to improve usability and meet product stakeholder requirements.","task"),
	("Create and carry out your own unit and UI tests to identify malfunctions.","task"),
	("Design the overall architecture of the front-end web application and create website and web dashboard layouts/user interface.","task"),
	("Write well designed, testable, efficient code in line with best software development practices.","task"),
	("Integrate data from various APIs i.e. integrate with back-end systems to create rich, data-driven web applications.","task"),
	("Create and maintain all necessary technical documentation.","task"),
	("Do things in an agile manner","skills"),
	("Embrace agile fundamentals and scrum","skills"),
	("Maintain, expand, scale, troubleshoot, debug and optimize the applications for maximum speed and scalability.","task"),
	("Keep up-to-date with emerging technologies/industry trends and apply them into operations and activities.","task"),
	("Would you like to ride on this exciting revolution? It's once in a lifetime. Don't miss it!","encourage_to_apply"),
	("Join our fast growing and dynamic team!","encourage_to_apply"),
	("Join our fast growing and dynamic team!","encourage_to_apply"),
	("Join our fast growing and dynamic team!","encourage_to_apply"),
	("Don't miss this opportunity to join an award winning team!","encourage_to_apply"),
	("Join now! Don't miss this exciting opportunity!","encourage_to_apply"),
	("5 Years of working experience in web frameworks","skill"),
	("Candidate must possess at least Professional Certificate, Diploma/Advanced/Higher/Graduate Diploma, Bachelor's Degree/Post Graduate Diploma/Professional Degree&nbsp;in any field.","skill"),
	("At least 3 Year(s) of working experience in the related field is required for this position","skill"),
	("health and dental benefits","benefits"),
	("work-life balance","benefits"),
	("attractive salary","benefits"),
	("we believe in good work-life balance","benefits"),
	("we promote good work-life balance","benefits"),
	("You will join a fastest-growing team","benefits"),
	("you will have a chance to join a fast-growing team","benefits"),
	("we have a good team spirit","benefits"),
	("Join a fast-growing and dynamic team","benefits"),
	("fast career growth","benefits"),
	("we promote fast career growth","benefits")
]

   classifier = classifiers.NaiveBayesClassifier(training2)

   textkk = "As our Front End Web Developer, you will be responsible for creating a fully functional user interface that enhances the experience of our customers. In this role, your input will be directly reflected in the products we develop and define pathways for future features to pursue. apidly design, prototype to meet the user requirements. Work closely with stakeholders and back-end developers to implement versatile front-end solutions. Design the overall architecture of the front-end web application and create website and web dashboard layouts/user interface. Write well designed, testable, efficient code in line with best software development practices. Candidates must possess at least a Bachelor's Degree in Computer Science. 5 Years of working experience in web frameworks. Proficiency in using React, HTML5, CSS3 and JavaScript GIT,Babel.js. Strong experience with Redux. You will join a fast-growing, dynamic and talented team with deep technological know-how. We have great team spirit and a diverse and creative culture. We believe in and promote good work-life balance. You'll have the chance to join one of the fastest growing e-commerce platforms in the world!"

   ll = split_into_sentences(textkk)

   types_of_sentences = []
   for xx in ll:
       blob=TextBlob(xx, classifier=classifier)
       types_of_sentences.append(blob.classify())
		
   # TODO implement
   return {
       'statusCode': 200,
       'body': json.dumps("")
   }