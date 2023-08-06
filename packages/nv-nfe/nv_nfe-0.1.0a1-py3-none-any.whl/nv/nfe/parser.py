from dataclasses import dataclass, field
from pathlib import Path
from typing import Union, Optional
import datetime

from .core import InvoiceWrapper, Invoice


__ALL__ = ['parse_nfe', 'load_nfe', 'NFe']


@dataclass(frozen=True)
class NFe:
    uid: str = field(compare=True)
    published_dt: datetime.datetime = field(compare=False)
    content: Invoice = field(compare=False)

    @classmethod
    def from_invoice_wrapper(cls, invoice_wrapper: InvoiceWrapper):
        return cls(uid=invoice_wrapper.security.info.unique_id,
                   published_dt=invoice_wrapper.security.info.published_date,
                   content=invoice_wrapper.content.invoice,
                   )


def parse_nfe(data: bytes, fail_safe=False) -> Optional[NFe]:
    try:
        nfe_wrapper = InvoiceWrapper.from_xml(data)
        return NFe.from_invoice_wrapper(nfe_wrapper)
    except Exception as e:
        if fail_safe:
            return None
        raise


def load_nfe(path: Union[Path, str], fail_safe=False) -> Optional[NFe]:
    fp = Path(path)
    assert fp.is_file() and fp.suffix == ".xml", "Path must point to a XML file"

    data = fp.read_bytes()
    return parse_nfe(data, fail_safe=fail_safe)
