# Challenges

## Port ranges

| Category    | External HAProxy port range | Kubernetes node port range | Notes                                      |
|-------------|-----------------------------|----------------------------|--------------------------------------------|
| crypto      | 1000-1099                   | 30000-30099                |                                            |
| linux       | 1100-1199                   | 30100-30199                |                                            |
| misc        | 1200-1299                   | 30200-30299                |                                            |
| jail        | 1300-1399                   | 30300-30399                |                                            |
| pwn         | 1400-1499                   | 30400-30499                |                                            |
| reverse     | 1500-1599                   | 30500-30599                |                                            |
| web         | 1600-1699                   | 30600-30699                | in case hostname based matching isn't used |
