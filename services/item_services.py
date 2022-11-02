from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import delete
from models.basemodels import Complete_Item_, Item_, Item_Simple_Data_, Item_Tax_Data_, Standard_Output
from models.connection import async_session
from models.tables import Error_Logs, Item, Item_Simple_Data, Item_Tax_Data
from sqlalchemy.future import select
from sqlalchemy.exc import DBAPIError, IntegrityError

# Contador para recursão
recursive_count = 0

async def add_item_(item_data, item_simple_data, item_tax_data):
    async with async_session() as session:
        try:
            item_id = None
            i_dt = item_data
            i_sd = item_simple_data
            i_td = item_tax_data

            # Adicionando na tabela 'item'
            session.add(Item(
                name=i_dt.name,
                price=i_dt.price,
                ean=i_dt.ean,
                weight=i_dt.weight,
                inventory=i_dt.inventory,
                is_active=i_dt.is_active
            ))
            await session.commit()
            # Obtendo id do usuário recém adicionado
            result = await session.execute(select(Item.id).where(Item.name == i_dt.name))
            item_id = result.scalars().first()
            
            # Adicionando na tabela item_simple_data
            session.add(Item_Simple_Data(
                item_id=item_id,
                cost=i_sd.cost,
                brand=i_sd.brand,
                category=i_sd.category,
                image_id=i_sd.image_id,
            ))
            await session.commit()

            # Adicionando na tabela item_tax_data
            session.add(Item_Tax_Data(
                item_id=item_id,
                ncm=i_td.ncm,
                measure=i_td.measure,
                origin=i_td.origin,
                discount=i_td.discount,
                cest=i_td.cest,
            ))
            await session.commit()

            return Standard_Output(message='Operação efetuada com sucesso.')
        except IntegrityError as error:
            await session.close()
            if item_id:
                await session.execute(delete(Item_Tax_Data).where(Item_Tax_Data.item_id == item_id))
                await session.execute(delete(Item_Simple_Data).where(Item_Simple_Data.item_id == item_id))
            raise HTTPException(status_code=400, detail='Item com dados duplicados. Corrija os dados e tente novamente')
        except DBAPIError as error:
            # Em caso de erro, apaga os dados que possivelmente foram inseridos.
            await session.close()
            if item_id:
                await session.execute(delete(Item_Tax_Data).where(Item_Tax_Data.item_id == item_id))
                await session.execute(delete(Item_Simple_Data).where(Item_Simple_Data.item_id == item_id))
            await session.execute(delete(Item).where(Item.name == i_dt.name))
            await session.commit()
            raise HTTPException(status_code=400, detail='Erro na requisição. Verifique os dados e tente novamente.')
        except Exception as error:
            # Em caso de erro, apaga os dados que possivelmente foram inseridos.
            await session.close()
            if item_id:
                await session.execute(delete(Item_Tax_Data).where(Item_Tax_Data.item_id == item_id))
                await session.execute(delete(Item_Simple_Data).where(Item_Simple_Data.item_id == item_id))
            await session.execute(delete(Item).where(Item.name == i_dt.name))
            session.add(Error_Logs(
                str(error), datetime.now(), None, 1, 'service add_item'
            ))
            await session.commit()
            raise HTTPException(status_code=500, detail='Erro no servidor. Estamos trabalhando para corrigir')

async def update_item_(item, item_simple_data, item_tax_data):
    async with async_session() as session:
        try:
            i, ist, itd = item, item_simple_data, item_tax_data
            result = await session.execute(
                select(Item, Item_Simple_Data, Item_Tax_Data)
                .join(Item_Simple_Data, Item.id == Item_Simple_Data.item_id)
                .join(Item_Tax_Data, Item.id == Item_Tax_Data.item_id)
                .where(Item.id == i.id)
            )
            result_item = result.first()

            # item, item_simple_db, item_tax_db
            item_db, item_sdb, item_tdb = result_item[0], result_item[1], result_item[2]

            item_db.name = i.name if i.name else item_db.name
            item_db.price = i.price if i.price else item_db.price
            item_db.ean = i.ean if i.ean else item_db.ean
            item_db.weight = i.weight if i.weight else item_db.weight
            item_db.inventory = i.inventory if i.inventory else item_db.inventory
            item_db.is_active = i.is_active if i.is_active else item_db.is_active

            item_sdb.cost = ist.cost if ist.cost else item_sdb.cost
            item_sdb.brand = ist.brand if ist.brand else item_sdb.brand
            item_sdb.category = ist.category if ist.category else item_sdb.category
            item_sdb.image_id = ist.image_id if ist.image_id else item_sdb.image_id

            item_tdb.ncm = itd.ncm if itd.ncm else item_tdb.ncm
            item_tdb.measure = itd.measure if itd.measure else item_tdb.measure
            item_tdb.origin = itd.origin if itd.origin else item_tdb.origin
            item_tdb.discount = itd.discount if itd.discount else item_tdb.discount
            item_tdb.cest = itd.cest if itd.cest else item_tdb.cest

            session.add(item_db)
            session.add(item_sdb)
            session.add(item_tdb)
            await session.commit()

            return Standard_Output(message='Operação efetuada com sucesso.')
        except TypeError as error:
            if "'NoneType' object is not subscriptable" in str(error):
                raise HTTPException(status_code=400, detail='O id de usuário não existe')
        except Exception as error:
            session.add(Error_Logs(
                str(error), datetime.now(), None, 1, 'service update_item_'
            ))
            await session.commit()
            raise HTTPException(status_code=500, detail='Erro no servidor. Estamos trabalhando para corrigir.')

async def get_item_(type_data, item_data):
    async with async_session() as session:
        try:
            td, itd = type_data, item_data
            if td == 'id':
                result = await session.execute(
                        select(Item, Item_Simple_Data, Item_Tax_Data)
                        .join(Item_Simple_Data, Item.id == Item_Simple_Data.item_id)
                        .join(Item_Tax_Data, Item.id == Item_Tax_Data.item_id)
                        .where(Item.id == itd)
                    )
                result_item = result.all()
            elif td == 'name':
                result = await session.execute(
                        select(Item, Item_Simple_Data, Item_Tax_Data)
                        .join(Item_Simple_Data, Item.id == Item_Simple_Data.item_id)
                        .join(Item_Tax_Data, Item.id == Item_Tax_Data.item_id)
                        .where(Item.name == itd)
                    )
                result_item = result.all()
            elif td == 'ean':
                result = await session.execute(
                        select(Item, Item_Simple_Data, Item_Tax_Data)
                        .join(Item_Simple_Data, Item.id == Item_Simple_Data.item_id)
                        .join(Item_Tax_Data, Item.id == Item_Tax_Data.item_id)
                        .where(Item.ean == itd)
                    )
                result_item = result.all()
            elif td == 'brand':
                result = await session.execute(
                        select(Item, Item_Simple_Data, Item_Tax_Data)
                        .join(Item_Simple_Data, Item.id == Item_Simple_Data.item_id)
                        .join(Item_Tax_Data, Item.id == Item_Tax_Data.item_id)
                        .where(Item_Simple_Data.brand == itd)
                    )
                result_item = result.all()
            elif td == 'category':
                result = await session.execute(
                        select(Item, Item_Simple_Data, Item_Tax_Data)
                        .join(Item_Simple_Data, Item.id == Item_Simple_Data.item_id)
                        .join(Item_Tax_Data, Item.id == Item_Tax_Data.item_id)
                        .where(Item_Simple_Data.category == itd)
                    )
                result_item = result.all()
            for i, item in enumerate(result_item):
                item_db = Item_(
                    id=item[0].id,
                    name=item[0].name,
                    price=item[0].price,
                    ean=item[0].ean,
                    weight=item[0].weight,
                    inventory=item[0].inventory,
                    is_active=item[0].is_active,
                )
                item_sdb = Item_Simple_Data_(
                    id=item[1].id,
                    item_id=item[1].item_id,
                    cost=item[1].cost,
                    brand=item[1].brand,
                    category=item[1].category,
                    image_id=item[1].image_id,
                )
                item_tdb = Item_Tax_Data_(
                    id=item[2].id,
                    item_id=item[2].item_id,
                    ncm=item[2].ncm,
                    measure=item[2].measure,
                    origin=item[2].origin,
                    discount=item[2].discount,
                    cest=item[2].cest
                )
                result_item[i] = Complete_Item_(
                    item=item_db,
                    item_simple_data=item_sdb,
                    item_tax_data=item_tdb
                )
            return result_item
        except Exception as error:
            session.add(Error_Logs(
                str(error), datetime.now(), None, 1, 'service _item_'
            ))
            await session.commit()
            raise HTTPException(status_code=500, detail='Erro no servidor. Estamos trabalhando para corrigir.')

async def delete_item_(id):
    async with async_session() as session:
        global recursive_count
        try:
            await session.execute(delete(Item_Simple_Data).where(Item_Simple_Data.item_id == id))
            await session.execute(delete(Item_Tax_Data).where(Item_Tax_Data.item_id == id))
            await session.execute(delete(Item).where(Item.id == id))
            await session.commit()
            return Standard_Output(message='Operação efetuada com sucesso')
        except Exception as error:
            await session.close()
            result = await session.execute(
                select(Item, Item_Simple_Data, Item_Tax_Data)
                .join(Item_Simple_Data, Item.id == Item_Simple_Data.item_id)
                .join(Item_Tax_Data, Item.id == Item_Tax_Data.item_id)
                .where(Item.id == id)
                )
            item = result.all()
            
            # Caso o item não tenha sido deletado, a função é chamada recursivamente por até
            # 3 vezes antes de gerar um erro.
            if len(item) > 0 and recursive_count < 3:
                recursive_count += 1
                await delete_item_(id)
            if recursive_count >= 3:
                recursive_count = 0
                session.add(Error_Logs(
                    str(error), datetime.now(), None, 1, 'service delete_item_'
                ))
                await session.commit()
                raise HTTPException(status_code=500, detail='Erro no servidor. Estamos trabalhando para corrigir.')
        