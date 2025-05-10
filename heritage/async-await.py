import asyncio
async def tarefa(numero:int) -> None:
    print(f'Inicio da tarefa {numero}')
    await asyncio.sleep(4)
    print(f'Fim da tarefa{numero}')

async def main() -> None:
    await asyncio.gather(tarefa(5), tarefa(6),tarefa(7))

if __name__ =='__main__':
    asyncio.run(main())