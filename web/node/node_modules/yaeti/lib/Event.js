function yaetiEvent(type)
{
	this.type = type;
	this.isTrusted = false;

	// Flag indicating this is not a DOM Event object.
	this._yaeti = true;
}

module.exports = yaetiEvent;
