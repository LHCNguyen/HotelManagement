import hashlib
import hmac
import urllib.parse

class vnpay_order:
    requestData = {}
    responseData = {}

    def get_payment_url(self, vnpay_payment_url, secret_key):
        inputData = sorted(self.requestData.items())
        queryString = ''
        hasData = ''
        seq = 0
        for key, val in inputData:
            if seq == 1:
                queryString = queryString + "&" + key + '=' + urllib.parse.quote_plus(str(val))
            else:
                seq = 1
                queryString = key + '=' + urllib.parse.quote_plus(str(val))

        print("Generated Query String: ", queryString)  # Log query string
        hashValue = self.__hmacsha512(secret_key, queryString)
        print("Generated Hash Value: ", hashValue)  # Log hash value
        payment_url = vnpay_payment_url + "?" + queryString + '&vnp_SecureHash=' + hashValue
        print("Generated Payment URL: ", payment_url)  # Log final URL
        return payment_url

    def validate_response(self, secret_key):
        try:
            vnp_SecureHash = self.responseData['vnp_SecureHash']
            if 'vnp_SecureHash' in self.responseData.keys():
                self.responseData.pop('vnp_SecureHash')

            if 'vnp_SecureHashType' in self.responseData.keys():
                self.responseData.pop('vnp_SecureHashType')

            inputData = sorted(self.responseData.items())
            hasData = ''
            seq = 0
            for key, val in inputData:
                if str(key).startswith('vnp_'):
                    if seq == 1:
                        hasData = hasData + "&" + str(key) + '=' + urllib.parse.quote_plus(str(val))
                    else:
                        seq = 1
                        hasData = str(key) + '=' + urllib.parse.quote_plus(str(val))

            print('Generated HasData:', hasData)  # Log dữ liệu Hash
            hashValue = self.__hmacsha512(secret_key, hasData)
            print('Generated Hash Value from HasData:', hashValue)  # Log hash value được tạo
            print('Input Hash from VNPAY:', vnp_SecureHash)  # Log hash từ VNPAY

            if vnp_SecureHash != hashValue:
                error_message = (
                    f"Chữ ký không hợp lệ! Debug thông tin:\n"
                    f" - HasData: {hasData}\n"
                    f" - HashValue (Generated): {hashValue}\n"
                    f" - InputHash (From VNPAY): {vnp_SecureHash}"
                )
                print(error_message)  # Quăng lỗi ra console
                raise ValueError(error_message)  # Quăng exception

            print("Chữ ký hợp lệ!")
            return True
        except Exception as e:
            print(f"Đã xảy ra lỗi trong quá trình validate: {e}")  # Log lỗi
            return False

    @staticmethod
    def __hmacsha512(key, data):
        byteKey = key.encode('utf-8')
        byteData = data.encode('utf-8')
        print(f"Generating HMAC with Key: {key} and Data: {data}")  # Log thông tin HMAC
        return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()