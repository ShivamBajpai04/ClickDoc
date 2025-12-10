import requests


class CommitData:
    diff: str
    jira_description: str
    jira_title: str


class doc_content:
    title: str
    body: str


class LLMOutputData:
    document_content: doc_content
    document_url: str


class OutputConfluenceData:
    confluence_link: str
    publication_status: str


def read_file_and_make_html_to_string_without_newlines(file_path: str) -> str:
    with open(file_path, "r") as file:
        content = file.read()
    return content.replace("\n", "")


SPACE_ID = "131074"

# Basic Auth token for Confluence API base64(email:token)
AUTH = "c2hpdmFtYmFqcGFpMDQud29ya0BnbWFpbC5jb206QVRBVFQzeEZmR0YwZllDaG5jVUxkak9mRExnQ3h2eUhPTDVROWVnLXJiME1fSlBZWk5DSGRSWWNtTE5LQjR1VXF4YjFBdXVTdTVnbGU2ZkpZWWYwLUZhQ1VKa0g2M040NlJBT2pQdUlra2tHdmNNOEN0NU1BczBreXh2Nkl4QzEyaUExaEhyS2R2Si11Q3lGT21KMFpoRTBNaEhTanFNekQ5MVl5cV9pSVZKV3pRQmctVzZWYmYwPTFGNDc1RDg2"

DATA = read_file_and_make_html_to_string_without_newlines("content.html")


class ClickDocService:
    def __init__(self):
        pass

    def consume_info_jira_bit_bucket(self, commit_id) -> CommitData:
        """
        Return
        diff, jira description,
        """
        pass

    def feed_intput_llm(self, commit_data: CommitData) -> LLMOutputData:
        pass

    def publish_output_confulence(
        self, llm_output_data: LLMOutputData
    ) -> OutputConfluenceData:
        content = llm_output_data.document_content
        url = llm_output_data.document_url

        print(f"Publishing to Confluence with content: {content} at {url}")
        result = OutputConfluenceData()
        url = None
        status = None
        if url == "" or url is None:
            url, status = self.create_page(content)
        else:
            url, status = self.update_page(content, url)
        result.confluence_link = url
        result.publication_status = status
        return result

    def create_page(self, content: doc_content) -> tuple[str, str]:
        url = "https://qrthing.atlassian.net/wiki/api/v2/pages"
        request_body = {
            "spaceId": "131074",  # Hard coded to push to a specific space
            "status": "draft",
            "title": content.title,
            "parentId": "",
            "body": {
                "representation": "storage",  # Hard coded to accept html like format
                "value": content.body,
            },
            "subtype": "",  # For pages that do not require live editing, keep blank
        }

        # add basic auth header
        headers = {
            "Authorization": f"Basic {AUTH}",
            "Content-Type": "application/json",
        }

        response = requests.post(url, headers=headers, json=request_body)

        if response.status_code == 200:
            data = response.json()
            links = data["_links"]
            page_url = links["webui"]
            base_url = links["base"]
            full_url = f"{base_url}{page_url}"
            return full_url, "created"
        else:
            return "", f"failed with status code {response.status_code}"

    def update_page(content: doc_content, page_url: str) -> tuple[str, str]:
        pass


def main():
    service = ClickDocService()
    llm_data = LLMOutputData()
    llm_data.document_content = doc_content()
    llm_data.document_content.title = "Sample Title"
    llm_data.document_content.body = DATA
    llm_data.document_url = None
    response = service.publish_output_confulence(llm_data)
    print(
        f"Confluence publish response: {response.confluence_link}, status: {response.publication_status}"
    )


main()

"""
Publishing to Confluence with content: <__main__.doc_content object at 0x0000019FEBDAB380> at None
Confluence publish response: https://qrthing.atlassian.net/wiki/pages/resumedraft.action?draftId=819201&draftShareId=e73dd936-6b4b-45fb-ab72-d917120e91df, status: created
"""
