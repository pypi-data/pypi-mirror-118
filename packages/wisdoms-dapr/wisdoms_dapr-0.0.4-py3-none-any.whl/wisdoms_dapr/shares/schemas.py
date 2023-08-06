import enum
import typing
import ipaddress
from pydantic import BaseModel, root_validator

from wisdoms_dapr.shares import data


class EnterpriseTypeEnum(str, enum.Enum):
    """企业类型枚举"""

    key = 'key'    # 重点企业类型


class EnterpriseInfoSchema(BaseModel):
    """基础企业信息"""

    id: str                                                # ID
    name: str                                              # 公司名称
    enterprise_type: typing.Optional[EnterpriseTypeEnum]   # 企业类型，包括重点企业，建议设为枚举类型，key表示重点企业
    industry_main_category: typing.Optional[str]           # 行业大类名称
    industry_main_category_code: typing.Optional[str]      # 行业大类code
    industry_sub_category: typing.Optional[str]            # 行业小类名称
    industry_sub_category_code: typing.Optional[int]       # 行业小类code
    province: typing.Optional[str]                         # 所在省份
    city: typing.Optional[str]                             # 所在市
    district: typing.Optional[str]                         # 所在区县
    park: typing.Optional[str]                             # 所在园区
    address: typing.Optional[str]                          # 详细地址
    public_network: typing.Optional[ipaddress.IPv4Network] # 公网网段，公网IP地址段类型，如：1.1.1.1/32
    domain: typing.Optional[str]                           # 域名
    website: typing.Optional[str]                          # 网址

    @root_validator
    def load_data(cls, values):
        """Validate data"""

        # validate administrative division
        province = values.get('province')
        if province:
            city = values.get('city')
            if city:
                if city not in data.CHINA_ADMINISTRATIVE_DIVISION[province]:
                    raise ValueError(f"{city} not in {province} province")
                else:
                    distinct = values.get('distinct')
                    if distinct and distinct not in data.CHINA_ADMINISTRATIVE_DIVISION[province][city]:
                        raise ValueError(f"{distinct} not in {province} province {city} city")
        else:
            if province not in data.CHINA_ADMINISTRATIVE_DIVISION:
                raise ValueError(f"invalid province {province}")

        return values
