import json
import unittest

from xrpl.models.currencies import XRP, IssuedCurrency
from xrpl.models.requests.book_offers import BookOffers

from ekspiper.processor.fetch_book_offers import BuildBookOfferRequestsProcessor

sample_transaction_json = """
{
  "ledger": {
    "accepted": true,
    "account_hash": "1BCE6A54FCC4ADDE1BE07E92665A23081AB23798A6E6ADD979157BD1778CAB6A",
    "close_flags": 0,
    "close_time": 710962411,
    "close_time_human": "2022-Jul-12 17:33:31.000000000 UTC",
    "close_time_resolution": 10,
    "closed": true,
    "hash": "128E62F87E422F78EA745D4489CA774D2411C9F024EEB109BD78B19E81A4E61A",
    "ledger_hash": "128E62F87E422F78EA745D4489CA774D2411C9F024EEB109BD78B19E81A4E61A",
    "ledger_index": "72959850",
    "parent_close_time": 710962410,
    "parent_hash": "A88DBFB1D7036D6FF8C327C0A0A519D63CC3432CE5B94028C78AF593BD4E097C",
    "seqNum": "72959850",
    "totalCoins": "99989401676275184",
    "total_coins": "99989401676275184",
    "transaction_hash": "4E81711912CE4A5B01E3D99B7CE61269CA560F795C0C7388E78913878D4F8068",
    "transactions": [
      {
        "Account": "r3Vh9ZmQxd3C5CPEB8q7VbRuMPxwuC634n",
        "Fee": "20",
        "Flags": 0,
        "LastLedgerSequence": 72959852,
        "Sequence": 80060618,
        "SigningPubKey": "03C71E57783E0651DFF647132172980B1F598334255F01DD447184B5D66501E67A",
        "TakerGets": {
          "currency": "USD",
          "issuer": "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
          "value": "77892.5"
        },
        "TakerPays": "250000000000",
        "TransactionType": "OfferCreate",
        "TxnSignature": "3045022100CC9AA1E70BD47336DFFC9F5A70FD06BF53346CD491E819242C6D925CC2BF7EE6022046C128F8750275E3BC7481D035D31BC4575C423D698B9A65FE9C0E81E97B5959",
        "hash": "EEC6AA1DA639A4C6C38E31D3D311244700D5BC199454C2AE59AD6555B446F7F8",
        "metaData": {
          "AffectedNodes": [
            {
              "ModifiedNode": {
                "FinalFields": {
                  "Flags": 0,
                  "IndexNext": "0",
                  "IndexPrevious": "0",
                  "Owner": "r3Vh9ZmQxd3C5CPEB8q7VbRuMPxwuC634n",
                  "RootIndex": "12F72282F74D437C2E76C4E57710E63779A1825D5A2090FF894FB9A22AF40AAE"
                },
                "LedgerEntryType": "DirectoryNode",
                "LedgerIndex": "12F72282F74D437C2E76C4E57710E63779A1825D5A2090FF894FB9A22AF40AAE"
              }
            },
            {
              "CreatedNode": {
                "LedgerEntryType": "DirectoryNode",
                "LedgerIndex": "4627DFFCFF8B5A265EDBD8AE8C14A52325DBFEDAF4F5C32E5B0B6711F888D00A",
                "NewFields": {
                  "ExchangeRate": "5b0b6711f888d00a",
                  "RootIndex": "4627DFFCFF8B5A265EDBD8AE8C14A52325DBFEDAF4F5C32E5B0B6711F888D00A",
                  "TakerGetsCurrency": "0000000000000000000000005553440000000000",
                  "TakerGetsIssuer": "0A20B3C85F482532A9578DBB3950B85CA06594D1"
                }
              }
            },
            {
              "CreatedNode": {
                "LedgerEntryType": "Offer",
                "LedgerIndex": "B177BC0668A17BB1D48EF1D6924ACD94E4A9065CE94011734EE15C4172207EE5",
                "NewFields": {
                  "Account": "r3Vh9ZmQxd3C5CPEB8q7VbRuMPxwuC634n",
                  "BookDirectory": "4627DFFCFF8B5A265EDBD8AE8C14A52325DBFEDAF4F5C32E5B0B6711F888D00A",
                  "Sequence": 80060618,
                  "TakerGets": {
                    "currency": "USD",
                    "issuer": "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
                    "value": "77892.5"
                  },
                  "TakerPays": "250000000000"
                }
              }
            },
            {
              "ModifiedNode": {
                "FinalFields": {
                  "Account": "r3Vh9ZmQxd3C5CPEB8q7VbRuMPxwuC634n",
                  "Balance": "178974365027",
                  "Flags": 0,
                  "OwnerCount": 6,
                  "Sequence": 80060619
                },
                "LedgerEntryType": "AccountRoot",
                "LedgerIndex": "F709D77D5D72E0C96CB029FCE21F3AF34E70ED0D8DB121B2CF961E64E582EEF2",
                "PreviousFields": {
                  "Balance": "178974365047",
                  "OwnerCount": 5,
                  "Sequence": 80060618
                },
                "PreviousTxnID": "49C65333B44E8DDDCAC5CE554A27439A4E9110B021D173FB98F6AD33E8729C0B",
                "PreviousTxnLgrSeq": 72959849
              }
            }
          ],
          "TransactionIndex": 0,
          "TransactionResult": "tesSUCCESS"
        }
      }
    ]
  },
  "ledger_hash": "128E62F87E422F78EA745D4489CA774D2411C9F024EEB109BD78B19E81A4E61A",
  "ledger_index": 72959850,
  "validated": true
}
"""


class BookOfferProcessorsTest(unittest.IsolatedAsyncioTestCase):
    async def test_build_book_offers_requests(self):
        input_entry = json.loads(sample_transaction_json)
        processor = BuildBookOfferRequestsProcessor()
        book_offer_requests = await processor.aprocess(
            input_entry,
        )

        expected_output = [
            BookOffers(
                taker_gets=IssuedCurrency(
                    currency="USD",
                    issuer="rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B",
                ),
                taker_pays=XRP(),
            ),
        ]

        self.assertEqual(len(expected_output), len(book_offer_requests))
        for actual_value, expected_value in zip(book_offer_requests, expected_output):
            self.assertEqual(actual_value.taker_gets, expected_value.taker_gets)
            self.assertEqual(actual_value.taker_pays, expected_value.taker_pays)
