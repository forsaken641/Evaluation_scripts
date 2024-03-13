import requests
from requests.auth import HTTPDigestAuth

token="sgp_local_723d3e6d5135ee30333cfeae9c2efde278e17e0d"

class Content:
    def __init__(self,software,branch,hash,type,file,token,message=''):
        self.software=software
        self.branch=branch
        self.hash=hash
        self.type=type
        self.file=file
        self.message=message
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
            query="context:global repo:^"+self.software+"$ rev:@"+self.branch+":"+self.hash+" file:"+self.file
            result = self.sourcegraph(query)
            result=result['data']['search']['results']['results'][0]['file']['content']

        if self.type=="diff":
            query = "context:global repo:^" + self.software + "$@"   + self.hash +" type:diff "+"message:'"+self.message+"'"
            #print(query)
            result=self.sourcegraph(query)
            result=result['data']['search']['results']['results'][0]['diffPreview']['value']
        return result


if __name__ == "__main__":
    #test=Content("linux","master","0f10757","file","drivers/input/serio/i8042.c",token)
    test=Content("linux","master","340d394a7","diff","",token,"fix crash at boot time")
    data=test.get_result()
    try:
        print(data)
    except:
        print('failed')