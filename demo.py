# from secure_auction import SecureAuction

# def main():
#     print("=== Secure Auction Demo ===")
#     auction = SecureAuction(duration=10)
    
#     # Register bidders
#     bidders = {
#         "Alice": 150,
#         "Bob": 200,
#         "Charlie": 175
#     }
    
#     print("\n=== Bidders Registration ===")
#     bidder_ids = {}
#     for name, bid in bidders.items():
#         bidder_ids[name] = auction.register_bidder(bid)
#         print(f"{name} registered with ID: {bidder_ids[name][:8]}...")
    
#     # Submit bids
#     print("\n=== Bidding Phase ===")
#     for name in bidders:
#         try:
#             auction.submit_bid(bidder_ids[name])
#             print(f"{name}'s bid submitted successfully")
#         except Exception as e:
#             print(f"{name} failed to bid: {str(e)}")
    
#     # Conclude auction
#     print("\n=== Auction Results ===")
#     try:
#         result = auction.conclude_auction()
#         if result["winner"]:
#             winner_name = [n for n, bid in bidder_ids.items() if bid == result["winner"]][0]
#             print(f"🏆 Winner: {winner_name} with bid ${result['winning_bid']}")
#             print("\nAll Valid Bids:")
#             for name, bid_id in bidder_ids.items():
#                 if bid_id in result["all_bids"]:
#                     print(f"• {name}: ${result['all_bids'][bid_id]}")
#         else:
#             print("No valid bids received")
#     except Exception as e:
#         print(f"Error concluding auction: {str(e)}")

# if __name__ == "__main__":
#     main()



from secure_auction import SecureAuction

def main():
    print("=== Secure Auction Demo ===")
    auction = SecureAuction(duration=10)
    
    # Register bidders
    bidders = {
        "Alice": 150,
        "Bob": 200,
        "Charlie": 175
    }
    
    print("\n=== Bidders Registration ===")
    bidder_ids = {}
    for name, bid in bidders.items():
        bidder_ids[name] = auction.register_bidder(bid)
        print(f"{name} registered with ID: {bidder_ids[name][:8]}...")
    
    # Submit bids
    print("\n=== Bidding Phase ===")
    for name in bidders:
        try:
            auction.submit_bid(bidder_ids[name])
            print(f"{name}'s bid submitted successfully")
        except Exception as e:
            print(f"{name} failed to bid: {str(e)}")
    
    # Conclude auction
    print("\n=== Auction Results ===")
    try:
        result = auction.conclude_auction()
        if result["winner"]:
            winner_name = [n for n, bid in bidder_ids.items() if bid == result["winner"]][0]
            print(f"🏆 Winner: {winner_name} with bid ${result['winning_bid']}")
            print("\nAll Valid Bids:")
            for name, bid_id in bidder_ids.items():
                if bid_id in result["all_bids"]:
                    print(f"• {name}: ${result['all_bids'][bid_id]}")
        else:
            print("No valid bids received")
    except Exception as e:
        print(f"Error concluding auction: {str(e)}")

if __name__ == "__main__":
    main()