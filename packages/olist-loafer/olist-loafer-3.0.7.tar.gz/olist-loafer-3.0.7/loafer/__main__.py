class Handler:
    async def handle(self, *args):
        print(args)
        return False


from loafer.ext.aws.routes import SNSQueueRoute

from loafer.managers import LoaferManager

common_provider_options = {
    "options": {
        "MaxNumberOfMessages": 1,
    },
}

routes = (
    SNSQueueRoute(
        "pool_election_service__seller_product__updated",
        common_provider_options,
        handler=Handler(),
    ),
    # KafkaRoute(
    #     "dev__channels__new_order__received",
    #     provider_options,
    #     handler=Handler(),
    #     message_translator=ProtobufSchemaMessageTranslator(new_order_pb2.NewOrder),
    # ),
)

manager = LoaferManager(routes)
manager.run()
