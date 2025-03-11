<<<<<<< HEAD
# GPU Stock Monitor

A comprehensive RTX 5080 and 5090 GPU stock tracking application with visual language model capabilities and autonomous AI agent integration.

## Overview

This application uses advanced multimodal AI techniques inspired by research papers like "Mind2Web", "WebArena", "VisualWebArena", and "Tree Search for Language Model Agents" to intelligently track RTX 5080 and 5090 GPU availability across multiple retailers.

The system can recognize special cases like Best Buy's "See Details" buttons that often appear for high-demand products instead of standard "Add to Cart" buttons.

## Features

- **Multi-retailer support**: Monitors multiple retailers simultaneously (Best Buy, Newegg, MSI, ASUS, B&H Photo)
- **Visual AI capabilities**: Uses advanced visual language models to identify product availability even when websites use different indicators
- **Reddit monitoring**: Tracks r/nvidia and r/buildapcsales subreddits for information about GPU availability and priority access programs
- **NowInStock integration**: Aggregates stock information from NowInStock.net for broader coverage
- **NVIDIA Priority Access tracking**: Special monitoring for NVIDIA's Priority Access Program and drawing opportunities
- **Intelligent notifications**: Get alerts when GPUs become available for purchase or when important information is posted
- **Smart scheduling**: Configurable check intervals based on time of day to balance between resource usage and responsiveness

## Supported Retailers

- **Best Buy**: Full support with special handling for "See Details" high-demand purchase flow
- **Newegg**: Monitors product listings with "Add to cart" vs "Auto Notify" detection
- **MSI website**: Tracks official MSI product pages and retailer links
- **ASUS website**: Monitors ASUS store with "Buy" and "Where to buy" button detection
- **B&H Photo**: Tracks availability with support for "Add to Cart" and "Pre-Order" states
- **NowInStock.net**: Aggregates availability data from multiple sources

## Reddit Monitoring

The system monitors Reddit communities for:
- New posts about RTX 5080 and 5090 availability
- Information about NVIDIA Priority Access Program
- Drawing opportunities and purchase events
- AI-analyzed summaries of important posts

## Project Structure

```
gpu-monitor
├── src
│   ├── __init__.py
│   ├── main.py                # Entry point of the application
│   ├── monitor.py             # Contains the GPUMonitor class
│   ├── notification.py        # Manages notifications
│   ├── utils.py               # Utility functions and constants
│   ├── chatbot
│   │   ├── __init__.py
│   │   ├── gpu_sourcing_chatbot.py  # GPU specialized chatbot
│   │   └── response_generator.py    # AI response generation
│   ├── retailers              # Directory for retailer implementations
│   │   ├── __init__.py
│   │   ├── base_retailer.py   # Base class for retailers
│   │   ├── bestbuy_retailer.py
│   │   ├── newegg_retailer.py
│   │   ├── msi_retailer.py
│   │   ├── asus_retailer.py
│   │   ├── bhphoto_retailer.py
│   │   ├── nowinstock_aggregator.py
│   │   └── reddit_monitor.py  # Reddit information tracking
│   └── ai_agent               # Directory for AI-related functionalities
│       ├── __init__.py
│       ├── visual_language_model.py  # Visual language model integration
│       ├── multimodal_agent.py       # Multimodal AI agent implementation
│       └── tree_search.py            # Tree search for complex web navigation
├── requirements.txt           # Project dependencies
├── .env                       # Environment variables
└── README.md                  # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd gpu-monitor
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables in the `.env` file. You'll need to include:
- Check intervals for different monitoring frequencies
- Reddit API credentials for the Reddit monitoring feature

```
# Retailer check intervals (seconds)
INTENSIVE_CHECK_INTERVAL=60
NORMAL_CHECK_INTERVAL=300
EXTENDED_CHECK_INTERVAL=3600
REDDIT_CHECK_INTERVAL=1800

# Reddit API credentials (for Reddit monitoring)
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
```

## Usage

To start the GPU monitoring application, run the following command:

```
python -m src.main
```
## To start the chatbot, run:

```
python -m src.main --chatbot
```

# To run regular monitorL

```
python -m src.main
```


The application will begin monitoring multiple retailers for RTX 5080 and 5090 GPUs and will notify you when products become available or when important information is posted on Reddit.

## Configuration

Edit the `.env` file to customize:

## Technical Details

The application uses:
- Selenium for web automation
- Visual language models for screenshot and HTML analysis
- Tree search algorithms for complex navigation tasks
- PRAW for Reddit API integration
- Multi-modal AI for understanding product availability signals

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## Credits

This project was inspired by research papers:
- "Mind2Web: Towards a Generalist Agent for the Web"
- "WebArena: A Realistic Web Environment for Building Autonomous Agents"
- "VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks"
- "Tree Search for Language Model Agents"

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
=======
# GPU_Stock_Monitor
>>>>>>> ba938ec2b55a45dcd30e27e90b5290b8e4c79c78
