# Widget Request Consumer

## Overview
This program processes widget operation requests and supports transferring data between AWS S3, SQS, and DynamoDB based on the provided configuration. Ensure the following prerequisites are met before running the program.


## Features
- Processes requests from either an **S3 bucket** or an **SQS queue**.
- Stores processed widgets in either an **S3 bucket** or a **DynamoDB table**.
- Supports three operations:
  - **Create**: Adds a new widget to the specified storage.
  - **Update**: Updates an existing widget's information.
  - **Delete**: Removes a widget from the storage.
- Logging to both console and log files for tracking request processing and errors.
  
## Example Scenarios

1. **S3 to S3**: Transfer widget operation requests from a source S3 bucket to a target S3 bucket.  
2. **S3 to DynamoDB**: Process widget operation requests from an S3 bucket and store results in DynamoDB.  
3. **SQS to DynamoDB**: Retrieve requests from an SQS queue and process them into a DynamoDB table.  
4. **SQS to S3**: Fetch requests from an SQS queue and store processed widgets in an S3 bucket.
   
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

1. **AWS CLI**  
   - The AWS Command Line Interface (CLI) must be installed and configured on your system.  
   - Set up credentials with appropriate permissions for accessing S3, SQS, and DynamoDB services.  
   [AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).

2. **Python 3.x**  
   - This program requires Python 3.x to run.  
   - Ensure Python is installed and accessible in your system’s PATH.  
   [Python Installation Guide](https://www.python.org/downloads/).

3. **AWS S3 Buckets** (Optional)  
   - **Request Bucket**: Stores incoming widget operation requests.  
   - **Target Bucket**: If S3 is chosen as the storage destination, this bucket stores processed widget data.  
   Example:  
     - `--sourcebucket`: The request bucket containing operation requests.  
     - `--target`: The bucket for processed widgets.  
   Ensure both buckets are created and accessible.

4. **DynamoDB Table** (Optional)  
   - If DynamoDB is used for widget storage, a DynamoDB table must be configured.  
   - The table should include necessary attributes, such as `widgetId` as the partition key or other required keys.  

5. **Source Queue URL** (Optional)  
   - If requests are retrieved from an SQS queue, provide the Queue URL or name.  
   - Ensure the queue is properly configured, and the IAM role or credentials have permissions to access it.

## Example Scenarios

1. **S3 to S3**: Transfer widget operation requests from a source S3 bucket to a target S3 bucket.  
2. **S3 to DynamoDB**: Process widget operation requests from an S3 bucket and store results in DynamoDB.  
3. **SQS to DynamoDB**: Retrieve requests from an SQS queue and process them into a DynamoDB table.  
4. **SQS to S3**: Fetch requests from an SQS queue and store processed widgets in an S3 bucket.

## Usage

Run the program using the command-line interface. Pass the required arguments based on the desired configuration:


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

3. Ensure you have your credentials properly configured:

## Usage
### Running the Program
The program processes requests from an S3 bucket and either stores or deletes widgets in another S3 bucket or DynamoDB table based on the operation requested.

Use the following command-line options to specify the source and target storage options:
The program processes requests from an S3 bucket and either stores or deletes widgets in another S3 bucket or DynamoDB table based on the operation requested.

```bash
python3 main.py [-rb <request-bucket>] [-rq <source queue>] [-wb <widget-bucket>] [-dt <dynamodb-table>]
```

- `-rq` or `--sourcequeue`: The SQS Queue URL from where requests are pulled.
  
- `-rb` or `--sourcebucket`: The S3 bucket where the requests are stored.

- `-wb` or `--target`: (Optional) The S3 bucket where the widget data will be stored (required if S3 storage is selected).

- `-dt` or `--dynamodb`: (Optional) The DynamoDB table name where widget data will be stored (required if DynamoDB storage is selected).

## Example

To process requests from `request-bucket` and store widget data in the `widget-bucket` using S3:

```bash
python3 main.py -rb <request-bucket> -wb <widget-bucket>
```

To process requests from `souce queue` and store widget data in DynamoDB:
```bash
python3 main.py -rq <queue_url> -dt <your-dynamodb-table>
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

