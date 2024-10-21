# Widget Request Consumer

## Overview
The **Widget Request Consumer** is a Python program designed to process requests from an S3 bucket, performing operations on widgets stored in either another S3 bucket or a DynamoDB table. The program supports creating, updating, and deleting widgets based on the requests, and logs operations for debugging and monitoring.

## Features
- Processes widget requests from an S3 request bucket.
- Handles widget data storage in either:
  - **S3 bucket**: For storing widget-related data in a specific target bucket.
  - **DynamoDB**: For storing widget data in a DynamoDB table.
- Supports three operations:
  - **Create**: Adds a new widget to the specified storage.
  - **Update**: Updates an existing widget's information.
  - **Delete**: Removes a widget from the storage.
- Logging to both console and log files for tracking request processing and errors.
  
## Directory Structure
```bash
.
├── logs/                   # Directory containing log files (created automatically)
├── S3_read.py              # Utility module for receiving and reading requests from S3
├── S3requesthandler.py      # Class for handling widget requests and storing data in S3
├── Dynamodbrequesthandler.py   # Class for handling widget requests and storing data in DynamoDB
├── main.py                 # Main script for processing requests
├── requirements.txt        # Python package requirements
└── README.md               # This file
```
## Prerequisites

Ensure you have the following installed on your system:

- **AWS CLI**: You need to have the AWS CLI installed and configured with appropriate credentials for accessing S3 and DynamoDB.
- **Python 3.x**: The program is written in Python and requires Python 3.x.
- **AWS S3 buckets**: You will need two S3 buckets:
    A request bucket that contains incoming widget operation requests.
    A target bucket (if using S3 as storage) to store processed widget data.
- **DynamoDB table** (optional): If you choose to use DynamoDB for widget storage, you will need a DynamoDB table set up with the necessary attributes (e.g., widgetId as the partition key).

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/10sajan10/consumer-program.git
   cd consumer-program
   ```
2. Install Dependencies:

  ```bash
   pip3 install -r requirements.txt
   ```

3. Ensure you have the AWS CLI set up and your credentials properly configured:

## Usage
### Running the Program
The program processes requests from an S3 bucket and either stores or deletes widgets in another S3 bucket or DynamoDB table based on the operation requested.

Use the following command-line options to specify the source and target storage options:
The program processes requests from an S3 bucket and either stores or deletes widgets in another S3 bucket or DynamoDB table based on the operation requested.

```bash
python main.py -ss <storage> -rb <request-bucket> [-wb <widget-bucket>] [-dt <dynamodb-table>]
```
- `-ss` or `--storage`: Specifies the storage strategy. Acceptable values are:
  - **S3** for using S3 buckets to store widget data.
  - **DynamoDB** for using DynamoDB to store widget data.
  
- `-rb` or `--source`: The S3 bucket where the requests are stored.

- `-wb` or `--target`: (Optional) The S3 bucket where the widget data will be stored (required if S3 storage is selected).

- `-dt` or `--dynamodb`: (Optional) The DynamoDB table name where widget data will be stored (required if DynamoDB storage is selected).

## Example

To process requests from `request-bucket` and store widget data in the `widget-bucket` using S3:

```bash
python main.py -ss S3 -rb request-bucket -wb widget-bucket
```

To process requests from `request-bucket` and store widget data in DynamoDB:
```bash
python main.py -ss DynamoDB -rb request-bucket -dt your-dynamodb-table
```
## Logs
Logs will be created in a `logs/` directory with the log file named after the current date (e.g., `2024-10-19.log`). All logs will be stored here, and they will also be displayed in the console during program execution.

## Modules
### S3RequestHandler
Handles the creation, update, and deletion of widget objects in a specified target S3 bucket. This module interacts with AWS S3 to perform operations based on the request received from the source bucket.

### DynamoDBRequestHandler
Handles the creation, update, and deletion of widget items in a DynamoDB table. This module interacts with AWS DynamoDB to perform operations based on the request received from the source bucket.

### S3RequestAndObjectReceiver
Utility module responsible for reading and fetching the smallest request object from the source S3 bucket. This module ensures efficient retrieval of requests for processing.

## Contributing
Feel free to open issues or submit pull requests if you'd like to contribute to this project. Make sure to write appropriate tests and documentation for your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For any inquiries or further assistance, please contact Sajan at sajan.neupane@usu.edu .

