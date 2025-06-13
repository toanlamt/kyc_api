from sqlalchemy.orm import Session
from app.models.kyc import KYC
from app.schemas.kyc import KYCCreate, KYCUpdate
from app.models.income import Income
from app.models.asset import Asset
from app.models.liability import Liability
from app.models.wealth_source import WealthSource
from datetime import datetime
from app.models.kyc import KYCStatus

def update_kyc(db: Session, kyc_id: int, data: KYCUpdate) -> KYC:
    kyc = db.query(KYC).filter(KYC.id == kyc_id).first()
    if not kyc:
        return None

    if data.market_experience is not None:
        kyc.market_experience = data.market_experience
    if data.risk_tolerance is not None:
        kyc.risk_tolerance = data.risk_tolerance
    if data.incomes is not None:
        db.query(Income).filter_by(kyc_id=kyc.id).delete()
        for income in data.incomes:
            db.add(Income(kyc_id=kyc.id, **income.dict()))
    if data.assets is not None:
        db.query(Asset).filter_by(kyc_id=kyc.id).delete()
        for asset in data.assets:
            db.add(Asset(kyc_id=kyc.id, **asset.dict()))
    if data.liabilities is not None:
        db.query(Liability).filter_by(kyc_id=kyc.id).delete()
        for liabilitie in data.liabilities:
            db.add(Liability(kyc_id=kyc.id, **liabilitie.dict()))
    if data.wealth_sources is not None:
        db.query(WealthSource).filter_by(kyc_id=kyc.id).delete()
        for wealth_source in data.wealth_sources:
            db.add(WealthSource(kyc_id=kyc.id, **wealth_source.dict()))

      # Update KYC status to Pending and set update timestamp
    kyc.status = KYCStatus.pending
    kyc.status_updated_at = datetime.utcnow()

    db.commit()
    db.refresh(kyc)
    return kyc