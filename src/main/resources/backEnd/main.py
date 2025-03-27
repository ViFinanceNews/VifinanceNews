from ViFinanceCrawLib.QualAna.QualAna import QualAnaIns
from ViFinanceCrawLib.QuantAna.QuantAna import QuantAnaIns
from ViFinanceCrawLib.QualAna.ArticleFactCheckUtility import ArticleFactCheckUtility
from ViFinanceCrawLib.article_database.ScrapeAndTagArticles import ScrapeAndTagArticles
from ViFinanceCrawLib.Summarizer.Summarizer import Summarizer
import time
import logging
import pprint
import pandas as pd
import numpy as np

# start_time = time.time()
# app = ScrapeAndTagArticles()

# articles_tag = app.search_and_scrape("Vietnam Economy in the first-fews month of 2025")
# for article in articles_tag:
#     print(article)


# end_time = time.time()
# elapsed_time = end_time - start_time  # Calculate elapsed time 

# print(f"Elapsed time: {elapsed_time:.4f} seconds")


# summarizer = Summarizer() 
# # the stopwords-dash was comming from this git-hub repository: https://github.com/stopwords/vietnamese-stopwords.git
# sample_text = """
#             Kinh tế là lĩnh vực nghiên cứu về cách thức sản xuất, phân phối và tiêu dùng các nguồn lực trong xã hội. Nó bao gồm nhiều khía cạnh như sản xuất hàng hóa và dịch vụ, thương mại quốc tế, tài chính, và sự phát triển kinh tế. Kinh tế có thể được chia thành hai nhánh chính: kinh tế vi mô và kinh tế vĩ mô. Kinh tế vi mô tập trung vào hành vi của các cá nhân và doanh nghiệp, trong khi kinh tế vĩ mô nghiên cứu các vấn đề toàn cầu như tăng trưởng kinh tế, lạm phát, thất nghiệp và chính sách tài chính.

# Một trong những yếu tố quan trọng trong phát triển kinh tế là năng lực sản xuất của nền kinh tế, bao gồm việc đầu tư vào công nghệ, cơ sở hạ tầng và nhân lực. Ngoài ra, thị trường lao động, hệ thống thuế và chính sách tài khóa cũng đóng vai trò quan trọng trong việc thúc đẩy hoặc làm giảm sự phát triển kinh tế.

# Kinh tế học không chỉ quan tâm đến việc tăng trưởng kinh tế mà còn chú trọng đến việc phân phối tài nguyên sao cho công bằng và bền vững, đặc biệt trong bối cảnh ngày càng nhiều vấn đề về môi trường và xã hội. Những vấn đề này đòi hỏi các chính sách kinh tế toàn diện và tầm nhìn dài hạn để đảm bảo phát triển bền vững.
#             """
# summary  = summarizer.summarize(sample_text, num_sentences=3)
# print("Tóm tắt:", summary)
# # summarizer.terminate() # Calling when stopping the model for saving cost


# test_quant = QuantAnaIns()
# test_quant.terminate()
# query = "Tình hình giá dầu thô hiện nay đang diễn biến ra sao trên thị trường quốc tế?"
# sources = [
#     "Giá dầu thô trên thị trường thế giới đang ghi nhận mức tăng cao trong những phiên giao dịch gần đây, chủ yếu do lo ngại về nguồn cung bị gián đoạn và nhu cầu năng lượng toàn cầu phục hồi mạnh mẽ sau giai đoạn suy giảm.",
    
#     "Thị trường dầu mỏ quốc tế chứng kiến mức giá leo thang khi OPEC+ quyết định duy trì mức cắt giảm sản lượng, đồng thời căng thẳng tại Trung Đông làm dấy lên nỗi lo về sự ổn định nguồn cung.",
    
#     "Trong vài tuần qua, giá dầu tăng do dự báo nhu cầu nhiên liệu tại châu Á tăng trưởng mạnh mẽ, đặc biệt là từ các nền kinh tế đang phục hồi sau đại dịch.",
    
#     "Giá dầu thô hiện tại phản ánh tác động từ việc tồn kho dầu của Mỹ giảm thấp hơn dự kiến, báo hiệu sự gia tăng trong nhu cầu tiêu thụ nội địa.",
    
#     "Mặc dù giá dầu có xu hướng tăng, một số chuyên gia cảnh báo rằng áp lực lạm phát và nguy cơ suy thoái kinh tế toàn cầu có thể làm giảm nhu cầu năng lượng trong dài hạn.",
    
#     "Sự kiện Nga tuyên bố hạn chế xuất khẩu dầu mỏ đã đẩy giá dầu lên mức cao nhất trong vòng sáu tháng qua, làm dấy lên lo ngại về căng thẳng địa chính trị leo thang.",
    
#     "Thị trường dầu mỏ đang chứng kiến những biến động mạnh, khi giá dầu chịu ảnh hưởng từ đồng USD mạnh lên và chính sách lãi suất cao của Cục Dự trữ Liên bang Mỹ.",
    
#     "Giá dầu thế giới ổn định trong ngắn hạn, tuy nhiên dự báo dài hạn cho thấy xu hướng tăng do nhu cầu chuyển đổi năng lượng và đầu tư vào các nguồn năng lượng tái tạo.",
    
#     "Một số nhà phân tích nhận định giá dầu có thể đạt đỉnh trong quý tới, do yếu tố cung - cầu đang ở trạng thái cân bằng hơn so với thời điểm đầu năm.",
    
#     "Thị trường dầu hiện nay đang chịu tác động từ cả yếu tố kỹ thuật và tâm lý, khi nhà đầu tư lo ngại về chính sách của các ngân hàng trung ương và nhu cầu tiêu thụ giảm dần."
# ]
# score = test_quant.compute_multi_semantic_similarity(source_articles=sources, query_article=None)
