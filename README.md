# E-Commerce Review Analysis

Python program to scrape real-world customer reviews for listed products on e-commerce websites like Amazon. The program scrapes these reviews and then transfers them to a Large Language Model of your choice (currently using Google Gemini) to generate market survey analysis in an unattended mode

## Usage

To use this program, you need to provide the API key for using Google Generative AI models and run `app.py`. It will ask for the Amazon ASIN code. Provide the ASIN code, and it will generate the analysis report, along with the reviews in the "reviews" directory.

## Requirements

- Python 3.x
- Necessary Python libraries (specified in `requirements.txt`)
- API key for Google Generative AI models

## Steps

1. Clone the repository or download the source code.
2. Install the required Python libraries using `pip install -r requirements.txt`.
3. Set up the API key for Google Generative AI models at `utils\llm_analyzer.py,` line 14
4. Run `app.py` using `python app.py`.
5. Enter the Amazon ASIN code when prompted.
6. Wait for the program to scrape the reviews and generate the analysis report.
7. The analysis report and reviews will be saved in the `reviews` directory.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html "GNU GPL v3")

## NOTICE

```
    E commerce review analysis
Python program to scrape real-world customer reviews for listed products on e-commerce websites like Amazon. The program scrapes these reviews and then transfers them to a Large Language Model of your choice (currently using Google Gemini) to generate market survey analysis in an unattended mode

    Copyright (C) 2024  Aishik Mukherjee

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
```
