import os
from rich.console import Console
from webscout import X0GPT
from webscout import exceptions
import re

# Initialize Console for rich output
console = Console()

# System Prompt (use for all interactions)
system_prompt = """
You are an exceptionally knowledgeable and patient AI tutor, capable of teaching any subject at any level of complexity. Your role is to create comprehensive, engaging, and deeply informative courses on various topics. When generating course content:

1. Provide thorough explanations that cover both fundamental concepts and advanced ideas.
2. Use clear, accessible language while maintaining academic rigor.
3. Incorporate a variety of teaching methods to cater to different learning styles.
4. Include numerous examples, analogies, and real-world applications to illustrate concepts.
5. Address potential misconceptions and common errors in understanding.
6. Encourage critical thinking and deeper exploration of the subject matter.
7. Maintain an encouraging and supportive tone throughout your teaching.

Your goal is to ensure that learners gain a complete and nuanced understanding of the topic, equipping them with the knowledge to apply concepts in various contexts and to pursue further learning independently.
"""

# Initialize X0GPT API clients
X0GPT_client_model_1 = X0GPT(
    is_conversation=False,
    timeout=1000000,
    max_tokens=8028,  # Adjust as needed
    intro=system_prompt,
#    model='X0GPT-8b'
)

X0GPT_client_model_2 = X0GPT(
    is_conversation=False,
    timeout=1000000,
    max_tokens=8028,  # Adjust as needed
    intro=system_prompt,
#    model='X0GPT-8b'
)

def generate_course(topic: str) -> dict:
    """Generates a comprehensive course outline based on the given topic using Model 1."""
    course_prompt = f"""
    Develop a comprehensive and in-depth course outline for the topic '{topic}'. The course should cater to beginners while also covering advanced concepts. Please provide:

    1. An engaging and thorough introduction to the topic (5-6 sentences):
       - Explain the significance of the topic
       - Briefly outline its historical context
       - Mention its relevance in contemporary contexts

    2. 8-10 main lessons or subtopics, organized in a logical learning sequence:
       - Ensure a smooth progression from foundational to advanced concepts
       - Include both theoretical and practical aspects of the topic

    3. For each lesson/subtopic:
       - Provide a clear and detailed description (4-5 sentences)
       - List 5-7 key concepts to be covered
       - Include 2-3 learning objectives
       - Suggest a practical example or real-world application
       - Propose a thought-provoking question or discussion point

    4. A comprehensive conclusion (5-6 sentences):
       - Summarize the main points covered in the course
       - Explain how the knowledge gained can be applied
       - Suggest areas for further study or exploration

    Format your response as a structured outline with clear headings and subheadings. Use markdown formatting for better readability.

    Example structure:
    # Course: [Topic]

    ## Introduction
    [Thorough introduction to the topic]

    ## Lesson 1: [Subtopic 1]
    - Description: [Detailed description of the lesson]
    - Key concepts: [List of 5-7 key concepts]
    - Learning objectives: [2-3 specific learning objectives]
    - Practical example: [Real-world application or example]
    - Discussion point: [Thought-provoking question]

    [Repeat for each lesson]

    ## Conclusion
    [Comprehensive summary and future directions]
    """
    try:
        course_response = X0GPT_client_model_1.chat(prompt=course_prompt)
        return {"course_outline": course_response}
    except exceptions.FailedToGenerateResponseError as e:
        return {"error": f"Failed to generate course outline: {e}"}

def generate_lesson(course_topic: str, subtopic: str) -> dict:
    """Generates detailed lesson content for the given subtopic using Model 1."""
    lesson_prompt = f"""
    Create a comprehensive and engaging lesson for the subtopic '{subtopic}' in the course about {course_topic}. Your lesson should be thorough, leaving no stone unturned in explaining the topic. Include:

    1. Introduction (1 paragraph):
       - Explain the significance of this subtopic within the broader course
       - Outline what the learner will gain from this lesson

    2. Historical Context (1-2 paragraphs):
       - Provide a brief history of the concept or theory
       - Explain how understanding has evolved over time

    3. Learning Objectives (4-6 clear, measurable objectives for the lesson)

    4. Key Concepts (list 6-8 main ideas with detailed explanations):
       - Define each concept clearly
       - Explain how these concepts interconnect

    5. In-depth Explanation:
       - Provide a comprehensive explanation of the subtopic (4-6 paragraphs)
       - Use multiple analogies or metaphors to explain complex ideas
       - Include mathematical formulas or scientific principles where applicable
       - Address common misconceptions or challenges related to the topic
       - Explain how this subtopic relates to other areas of the main topic

    6. Real-world Examples and Applications:
       - Include at least three detailed practical examples relevant to the subtopic
       - Explain how these examples illustrate the concepts
       - Discuss potential real-world applications or technologies based on these concepts

    7. Interactive Elements:
       - Suggest 2-3 hands-on activities, thought experiments, or mini-projects related to the topic
       - Provide step-by-step instructions for at least one of these activities

    8. Case Studies (if applicable):
       - Present 1-2 relevant case studies that demonstrate the application of the concepts
       - Analyze these cases to reinforce understanding

    9. Summary (1 paragraph summarizing the main points and their significance)

    10. Further Reading:
        - Suggest 4-5 resources (books, articles, videos, research papers) for students who want to explore the topic further
        - Briefly explain what each resource offers

    11. Reflection and Critical Thinking:
        - Provide 3-4 thought-provoking questions to encourage critical thinking about the topic
        - Suggest potential areas for future research or exploration in this subtopic

    Format your response using markdown for better readability and structure. Use headings, subheadings, bullet points, and numbered lists to organize the content clearly.
    """
    try:
        lesson_response = X0GPT_client_model_1.chat(prompt=lesson_prompt)
        return {"lesson_content": lesson_response}
    except exceptions.FailedToGenerateResponseError as e:
        return {"error": f"Failed to generate lesson content: {e}"}

def generate_quiz(course_topic: str, subtopic: str) -> dict:
    """Generates a comprehensive quiz to test understanding of the lesson using Model 2."""
    quiz_prompt = f"""
    Design a comprehensive and challenging quiz to evaluate deep understanding of the lesson on '{subtopic}' in the {course_topic} course. The quiz should test not only recall but also application, analysis, and synthesis of knowledge. Include:

    1. 8 Multiple-choice Questions:
       - Ensure questions cover different aspects of the subtopic
       - Include at least three questions that require application of knowledge to new situations
       - One question should involve interpreting a graph, diagram, or data set related to the topic

    2. 3 True/False Questions:
       - Make sure these questions address common misconceptions
       - Include a "justify your answer" component for each T/F question

    3. 4 Short Answer Questions:
       - Two questions should test basic understanding and recall
       - Two questions should require deeper analysis, synthesis, or application of concepts

    4. 2 Essay Questions:
       - One question should ask for an in-depth explanation of a core concept
       - One question should require the student to apply multiple concepts to analyze a complex scenario

    5. 1 Numerical Problem (if applicable to the topic):
       - Present a problem that requires quantitative reasoning and calculation
       - Provide step-by-step instructions for solving

    For each question:
    - Provide the correct answer
    - Include a detailed explanation of why the answer is correct
    - For incorrect options in multiple-choice questions, explain why they are wrong
    - Suggest further areas of study related to each question

    Format your response using markdown for better readability and structure. Use headings and subheadings to organize the content clearly.
    """
    try:
        quiz_response = X0GPT_client_model_2.chat(prompt=quiz_prompt)
        return {"quiz_content": quiz_response}
    except exceptions.FailedToGenerateResponseError as e:
        return {"error": f"Failed to generate quiz content: {e}"}

def create_course_structure(topic: str) -> dict:
    """Creates the directory structure and returns the generated course content."""
    # Generate course outline
    course_data = generate_course(topic)
    if "error" in course_data:
        return {"error": f"Error generating course outline: {course_data['error']}"}

    # Extract subtopics from the course outline
    subtopics = re.findall(r"## Lesson \d+: (.+?)\n", course_data["course_outline"])
    
    lessons = []
    quizzes = []

    for index, subtopic in enumerate(subtopics, start=1):
        # Generate lesson content
        lesson_data = generate_lesson(topic, subtopic)
        if "error" in lesson_data:
            continue
        lessons.append(lesson_data["lesson_content"])

        # Generate quiz content
        quiz_data = generate_quiz(topic, subtopic)
        if "error" in quiz_data:
            continue
        quizzes.append(quiz_data["quiz_content"])

    return {
        "course_outline": course_data.get("course_outline", ""),
        "lessons": lessons,
        "quizzes": quizzes
    }


if __name__ == "__main__":
    # Example usage
    topic = input("Enter the course topic: ")
    create_course_structure(topic)
