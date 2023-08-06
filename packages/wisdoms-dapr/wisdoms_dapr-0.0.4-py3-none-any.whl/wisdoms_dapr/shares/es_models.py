from elasticsearch_dsl import InnerDoc, field


class EnterpriseBaseInfoInnerDoc(InnerDoc):
    """共享企业基础信息"""

    # ************ 企业共享基础信息 ************
    id = field.Keyword()                                      # ID
    name = field.Keyword()                                    # 公司名称
    enterprise_type = field.Keyword()                         # 企业类型，包括重点企业，建议设为枚举类型，key表示重点企业
    industry_main_category = field.Keyword()                  # 行业大类名称
    industry_main_category_code = field.Keyword()             # 行业大类code
    industry_sub_category = field.Keyword()                   # 行业小类名称
    industry_sub_category_code = field.Keyword()              # 行业小类code
    province = field.Keyword()                                # 所在省份
    city = field.Keyword()                                    # 所在市
    district = field.Keyword()                                # 所在区县
    park = field.Keyword()                                    # 所在园区
    address = field.Text(fields={'keyword': field.Keyword()}) # 详细地址
    public_network = field.IpRange()                          # 公网网段，公网IP地址段类型，如：1.1.1.1/32
    domain = field.Keyword()                                  # 域名
    website = field.Keyword()                                 # 网址
