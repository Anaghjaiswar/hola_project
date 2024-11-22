import pusher

pusher_client = pusher.Pusher(
  app_id='1899783',
  key='36355bb5842f58e6b341',
  secret='48d90539776618f9dd3c',
  cluster='mt1',
  ssl=True
)

pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})