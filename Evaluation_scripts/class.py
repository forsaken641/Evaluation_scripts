import requests
from requests.auth import HTTPDigestAuth

token="sgp_local_723d3e6d5135ee30333cfeae9c2efde278e17e0d"
#依次输入软件名、查询语句、查询类型、token
class Content:
    def __init__(self,software,query,type,token=''):
        self.software=software
        self.query=query
        self.type=type
        self.token=token

    def sourcegraph(self,query):

        url = "http://222.20.126.205/.api/graphql"
        headers = {
            "Authorization": f"token {self.token}",
            "Content-Type": "application/json",
        }
        data = {
            "query": """
              query ($query: String!) {
                search(query: $query, version: V2) {
                  results {
                    results {
                      __typename
                      ... on FileMatch {
                        ...FileMatchFields
                      }
                      ... on CommitSearchResult {
                        ...CommitSearchResultFields
                      }
                      ... on Repository {
                        ...RepositoryFields
                      }
                    }
                    limitHit
                    cloning {
                      name
                    }
                    missing {
                      name
                    }
                    timedout {
                      name
                    }
                    matchCount
                    elapsedMilliseconds
                    ...SearchResultsAlertFields
                  }
                }
              }

              fragment FileMatchFields on FileMatch {
                repository {
                  name
                  url
                }
                file {
                  name
                  path
                  url
                  content
                  commit {
                    oid
                  }
                }
                lineMatches {
                  preview
                  lineNumber
                  offsetAndLengths
                  limitHit
                }
              }

              fragment CommitSearchResultFields on CommitSearchResult {
                messagePreview {
                  value
                  highlights {
                    line
                    character
                    length
                  }
                }
                diffPreview {
                  value
                  highlights {
                    line
                    character
                    length
                  }
                }
                label {
                  html
                }
                url
                matches {
                  url
                  body {
                    html
                    text
                  }
                  highlights {
                    character
                    line
                    length
                  }
                }
                commit {
                  repository {
                    name
                  }
                  oid
                  url
                  subject
                  author {
                    date
                    person {
                      displayName
                    }
                  }
                }
              }

              fragment RepositoryFields on Repository {
                name
                url
                externalURLs {
                  serviceType
                  url
                }
                label {
                  html
                }
              }

              fragment SearchResultsAlertFields on SearchResults {
                alert {
                  title
                  description
                  proposedQueries {
                    description
                    query
                  }
                }
              }
            """,
            "variables": {
                "query": query,
            }
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            print(response.headers)
            return None

    def get_result(self):
        if self.type=="file":
            query=self.query
            result = self.sourcegraph(query)
            result=result['data']['search']['results']['results'][0]['file']['content']

        if self.type=="diff":
            query = self.query
            #print(query)
            result=self.sourcegraph(query)
            result=result['data']['search']['results']['results'][0]['diffPreview']['value']
        return result


if __name__ == "__main__":
    test=Content("linux","context:global repo:^linux$ rev:@master:0f10757 file:drivers/input/serio/i8042.c","file",token)
    #test = Content("linux","context:global repo:^linux$@340d394a7 type:diff message:\"fix crash at boot time\"","diff",token)
    data=test.get_result()
    try:
        print(data)
    except:
        print('failed')