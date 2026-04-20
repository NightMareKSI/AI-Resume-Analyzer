def get_skill_recommendations(missing_skills):

    recommendations = {

        "python": "Learn Python programming for automation, data science, and backend development",

        "java": "Understand object-oriented programming and enterprise application development",

        "c++": "Learn system-level programming and performance optimization",

        "sql": "Practice writing queries for database management and data retrieval",

        "machine learning": "Study algorithms for prediction, classification, and data modeling",

        "deep learning": "Learn neural networks and frameworks like TensorFlow or PyTorch",

        "nlp": "Explore text processing, chatbots, and language understanding techniques",

        "data analysis": "Learn data cleaning, visualization, and statistical analysis",

        "react": "Build interactive user interfaces using React framework",

        "nodejs": "Develop backend APIs and server-side applications",

        "mongodb": "Learn NoSQL database design and document storage",

        "aws": "Understand cloud computing services for scalable deployment",

        "docker": "Learn containerization for packaging and deploying applications",

        "tensorflow": "Build machine learning and deep learning models",

        "kubernetes": "Learn container orchestration for large-scale systems",
        
        "pytorch": "Develop neural networks and AI applications",

        "html": "Learn web page structure and semantic markup",

        "css": "Style web pages using layouts, flexbox, and responsive design",

        "javascript": "Learn client-side scripting and web interactivity",

        "git": "Master version control, branching, and collaboration workflows",

        "linux": "Understand command-line tools and system administration",
        
        "c#": "Develop applications using the C# language and .NET framework",
        
        "scala": "Learn functional programming and big data processing",
        
        "r": "Master statistical programming and data analysis",
        
        "spark": "Learn distributed computing and big data processing",
        
        "hadoop": "Understand distributed file systems and MapReduce",
        
        "selenium": "Automate web testing and browser interactions",
        
        "postman": "Learn API testing and debugging techniques",
        
        "jenkins": "Set up continuous integration and deployment pipelines",
        
        "azure": "Master Microsoft cloud services and deployment",
        
        "gcp": "Learn Google Cloud Platform services",

    }

    suggested = {}

    for skill in missing_skills:
        # Convert skill to lowercase for matching
        skill_lower = skill.lower().strip()
        
        if skill_lower in recommendations:
            suggested[skill] = recommendations[skill_lower]

    return suggested