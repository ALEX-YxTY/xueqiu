import urllib.request
import urllib.parse


class HttpRequest:
    def __init__(self):
        pass

    @staticmethod
    def get(url, data, header={}, decode='gbk'):
        """
        HttpRequest.Get(url,data）
        :param decode:  编码,默认GBK
        :param url:
        :param data:
        :param header: 头部
        :return:
        """
        data = urllib.parse.urlencode(data, 'utf-8')
        new_url = url + "?" + data
        req = urllib.request.Request(url=new_url, headers=header)
        result = urllib.request.urlopen(req)
        response = result.read()
        # print(response)
        return response.decode(decode)

    @staticmethod
    def post(url, data):
        """
        HttpRequest.Post(url,data）
        :param url:
        :param data:
        :return:
        """
        data = urllib.parse.encode(data)
        data = data.encode('utf8')
        new_url = urllib.request.Request(url, data)
        result = urllib.request.urlopen(new_url)
        response = result.read()
        return response.decode('utf8')
        return response


if __name__ == '__main__':
    print('this is ok')
