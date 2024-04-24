from agents import MarketingAnalysisAgents
from tasks import MarketingAnalysisTasks
from crewai import Crew
from dotenv import load_dotenv
load_dotenv()


tasks = MarketingAnalysisTasks()
agents = MarketingAnalysisAgents()

product_website = "www.temperaturecontrolcoffeemug.com"
product_details = "Our temperature control coffee mug allows you to set your preferred drinking temperature and keep it perfect for up to 3 hours. Ideal for coffee, tea, and other beverages. Features a sleek design with a smart LED display, and it's made from durable stainless steel. Looking to highlight its convenience for busy professionals and its technology in a new Instagram campaign."

# Create Agents
product_competitor_agent = agents.product_competitor_agent()
strategy_planner_agent = agents.strategy_planner_agent()
creative_agent = agents.creative_content_creator_agent()
# Create Tasks
website_analysis = tasks.product_analysis(
    product_competitor_agent, product_website, product_details)
market_analysis = tasks.competitor_analysis(
    product_competitor_agent, product_website, product_details)
campaign_development = tasks.campaign_development(
    strategy_planner_agent, product_website, product_details)
write_copy = tasks.instagram_ad_copy(creative_agent)

# Create Crew responsible for Copy
copy_crew = Crew(
    agents=[
        product_competitor_agent,
        strategy_planner_agent,
        creative_agent
    ],
    tasks=[
        website_analysis,
        market_analysis,
        campaign_development,
        write_copy
    ],
    verbose=True,
    # Remove this when running locally. This helps prevent rate limiting with groq.
    max_rpm=1
)

ad_copy = copy_crew.kickoff()

# Create Crew responsible for Image
senior_photographer = agents.senior_photographer_agent()
chief_creative_diretor = agents.chief_creative_diretor_agent()
# Create Tasks for Image
take_photo = tasks.take_photograph_task(
    senior_photographer, ad_copy, product_website, product_details)
approve_photo = tasks.review_photo(
    chief_creative_diretor, product_website, product_details)

image_crew = Crew(
    agents=[
        senior_photographer,
        chief_creative_diretor
    ],
    tasks=[
        take_photo,
        approve_photo
    ],
    verbose=True,
    # Remove this when running locally. This helps prevent rate limiting with groq.
    max_rpm=1
)

image = image_crew.kickoff()

# Print results
print("\n\n########################")
print("## Here is the result")
print("########################\n")
print("Your post copy:")
print(ad_copy)
print("'\n\nYour midjourney description:")
print(image)
